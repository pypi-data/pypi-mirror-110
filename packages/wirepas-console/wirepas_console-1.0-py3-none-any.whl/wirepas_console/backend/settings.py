#!/usr/bin/env python3

from sqlite3.dbapi2 import Connection
import sys
import os
import sqlite3


# Alias for database-related errors
Error = sqlite3.Error


class MqttConnection:
    """MQTT connection settings"""

    def __init__(self, name, host, port, username, password, use_tls):
        self.name = name
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.use_tls = bool(use_tls)

    @classmethod
    def from_row(cls, row):
        return cls(
            name=row["name"],
            host=row["host"],
            port=row["port"],
            username=row["username"],
            password=row["password"],
            use_tls=row["use_tls"],
        )


class MqttConnections:
    """A collection of MQTT connection settings, backed by SQLite3 database"""

    def __init__(self, db_path):
        self.db_path = db_path
        self.ram_only = False
        self._db_conn = None

    def _open_db(self):
        if not self._db_conn:
            try:
                # Try to create database directory, if it does not exist
                os.makedirs(self.db_path, exist_ok=True)

                # Open or create an SQLite3 database file on disk
                self._db_conn = sqlite3.connect(
                    os.path.join(self.db_path, "connections.sqlite3")
                )
                self.ram_only = False
            except (OSError, sqlite3.Error):
                # Could not access database file, store in RAM only
                self._db_conn = sqlite3.connect(":memory:")
                self.ram_only = True

        # Use row factory to access query results by column name
        self._db_conn.row_factory = sqlite3.Row

    def _close_db(self):
        if not self.ram_only:
            # Don't keep disk-based SQLite3 database file open
            self._db_conn.close()
            self._db_conn = None

    def __iter__(self):
        self._open_db()

        try:
            # Read stored connection settings from SQLite3 database file
            conn_list = []
            for row in self._db_conn.execute(
                """
                SELECT rowid, name, host, port, username, password, use_tls
                    FROM connections ORDER BY rowid
                """
            ):
                try:
                    conn_list.append((row["rowid"], MqttConnection.from_row(row)))
                except (ValueError, TypeError):
                    # Skip invalid database rows, e.g. with NULL columns
                    pass
        finally:
            self._close_db()

        return iter(conn_list)

    def load(self):
        self._open_db()

        try:
            # Create the "connections" table if it doesn't exist yet
            self._db_conn.execute(
                """
                CREATE TABLE IF NOT EXISTS connections
                    (name TEXT, host TEXT, port INTEGER, username TEXT,
                    password TEXT, use_tls BOOLEAN)
                """
            )

            # Save changes
            self._db_conn.commit()
        finally:
            self._close_db()

    def add(self, mqtt_connection):
        self._open_db()

        try:
            # Store connection settings and create a new connection ID
            cur = self._db_conn.execute(
                """
                INSERT INTO connections
                    (name, host, port, username, password, use_tls) VALUES
                    (:name, :host, :port, :username, :password, :use_tls)
                """,
                {
                    "name": mqtt_connection.name,
                    "host": mqtt_connection.host,
                    "port": mqtt_connection.port,
                    "username": mqtt_connection.username,
                    "password": mqtt_connection.password,
                    "use_tls": mqtt_connection.use_tls,
                },
            )

            # Get ID of inserted row
            conn_id = cur.lastrowid

            # Save changes
            self._db_conn.commit()
        finally:
            self._close_db()

        return conn_id

    def delete(self, conn_id):
        self._open_db()

        try:
            # Delete all stored settings for a given connection ID
            cur = self._db_conn.execute(
                """
                DELETE FROM connections WHERE rowid=:conn_id
                """,
                {"conn_id": conn_id},
            )

            if cur.rowcount == 0:
                # Connection ID not found
                raise KeyError(conn_id)

            # Save changes
            self._db_conn.commit()
        finally:
            self._close_db()

    def get(self, conn_id):
        self._open_db()

        try:
            # Get connection settings for a given connection ID
            row = self._db_conn.execute(
                """
                SELECT name, host, port, username, password, use_tls
                    FROM connections WHERE rowid=:conn_id LIMIT 1
                """,
                {"conn_id": conn_id},
            ).fetchone()

            if row is None:
                # Connection ID not found
                raise KeyError(conn_id)
        finally:
            self._close_db()

        return MqttConnection.from_row(row)
