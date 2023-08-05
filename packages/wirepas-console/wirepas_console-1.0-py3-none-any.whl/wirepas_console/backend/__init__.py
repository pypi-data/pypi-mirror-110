#!/usr/bin/env python3

import sys
import os
import json
import random

import tornado.ioloop
import tornado.web
import tornado.websocket

from . import mqtt_connection
from . import settings


# List of currently open WebSocket connections
tornado_websocket = {}

# Connections list object, to add, delete and query stored connections
connections_list = None

# Connection ID of currently open MQTT connection
active_conn_id = None

# MQTT connection object
mqtt_conn = None


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # Allow HTTP access from anywhere
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type"
        )
        self.set_header("Access-Control-Allow-Methods", " PUT, DELETE, OPTIONS")

    def options(self):
        self.set_status(204)  # 204 No Content
        self.finish()


class MainHandler(BaseHandler):
    def get(self):
        path = self.request.uri

        print("MainHandler: %s" % path)  # DEBUG

        if (not path.startswith("/templates/")) or ("/../" in path):
            # Error, invalid path
            raise tornado.web.HTTPError(404)  # 404 Not Found

        # Strip "/templates/" from the path
        path = path[11:]

        # Set the correct MIME type
        if path.endswith(".html"):
            mime_type = "text/html"
        elif path.endswith(".css"):
            mime_type = "text/css"
        elif path.endswith(".js"):
            mime_type = "text/javascript"
        else:
            mime_type = "application/octet-stream"

        self.set_header("Content-Type", mime_type)

        # Set XSRF cookie
        self.xsrf_token

        self.render(path)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        # Allow WebSocket access from anywhere
        return True

    def open(self):
        global tornado_websocket
        tornado_websocket[self] = True

        print("WebSocketHandler: opened")  # DEBUG

    def on_message(self, message):
        print("WebSocketHandler: got message: " + message)  # DEBUG

    def on_close(self):
        global tornado_websocket

        del tornado_websocket[self]

        print("WebSocketHandler: closed")  # DEBUG


class StartupHandler(BaseHandler):
    def post(self):
        global active_conn_id
        global mqtt_conn

        print("StartupHandler: POST %s" % self.request.uri)  # DEBUG
        print("StartupHandler: body: %s" % repr(self.request.body))  # DEBUG

        # Clear active connection
        active_conn_id = None

        if mqtt_conn:
            mqtt_conn.close()
            mqtt_conn = None

        resp = {"st": "ok"}

        # Produce response as JSON
        print("StartupHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class ListMqttHandler(BaseHandler):
    def get(self):
        global connections_list
        global active_conn_id

        print("ListMqttHandler: GET %s" % self.request.uri)  # DEBUG
        print("ListMqttHandler: body: %s" % repr(self.request.body))  # DEBUG

        # List all gateways connected to an MQTT broker
        # and all sinks under those gateways
        resp = {
            "st": "ok",
            "conn_id": active_conn_id,
            "mqtt": [
                {
                    "id": c[0],
                    "name": c[1].name,
                    "host": c[1].host,
                    "port": c[1].port,
                    "username": c[1].username,
                    # "password" not returned
                    "use_tls": c[1].use_tls,
                }
                for c in connections_list
            ],
        }

        # Produce response as JSON
        print("ListMqttHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class GetMqttHandler(BaseHandler):
    def get(self):
        global connections_list
        global active_conn_id

        print("GetMqttHandler: GET %s" % self.request.uri)  # DEBUG
        print("GetMqttHandler: body: %s" % repr(self.request.body))  # DEBUG

        # Return active connection ID
        resp = {"st": "ok", "conn_id": active_conn_id}

        # Produce response as JSON
        print("GetMqttHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class AddMqttHandler(BaseHandler):
    def post(self):
        global connections_list
        global active_conn_id
        global mqtt_conn

        print("AddMqttHandler: POST %s" % self.request.uri)  # DEBUG
        print("AddMqttHandler: body: %s" % repr(self.request.body))  # DEBUG

        try:
            # Convert posted data from JSON
            data = tornado.escape.json_decode(self.request.body)

            # Parse fields
            conn = settings.MqttConnection(
                data["name"],
                data["host"],
                int(data["port"]),
                data["username"],
                data["password"],
                data.get("use_tls", False),  # Optional, False by default
            )
        except:
            raise tornado.web.HTTPError(400)  # 400 Bad Request

        if not mqtt_conn:
            try:
                # Open MQTT connection
                mqtt_conn = mqtt_connection.MqttConnection(
                    conn.host, conn.port, conn.username, conn.password, conn.use_tls
                )
            except:
                raise tornado.web.HTTPError(400)  # 400 Bad Request

            # Save MQTT connection settings to a list of previous connections
            active_conn_id = connections_list.add(conn)

            # Send a WebSocket event to tell that the connection
            # settings have changed
            send_ws_event("connections_list_change")
        else:
            # Error, MQTT connection already open
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        # DEBUG: This does not work, due to the
        # internal thread in the MQTT library
        #
        # def rx_callback(data):
        #     payload = data.data_payload
        #     addr = data.source_address
        #     src_ep = data.source_endpoint
        #     dest_ep = data.destination_endpoint
        #     travel_time = data.travel_time_ms / 1000.0
        #     qos = mqtt_connection.Qos(data.qos)
        #     send_ws_data_event(
        #         "rx", payload, addr, src_ep, dest_ep, travel_time, qos
        #     )
        #
        # mqtt_conn.set_data_rx_callback(rx_callback)

        # Return connection ID of added connection
        resp = {"st": "ok", "conn_id": active_conn_id}

        # Produce response as JSON
        print("AddMqttHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class DelMqttHandler(BaseHandler):
    def post(self):
        global connections_list
        global active_conn_id
        global mqtt_conn

        print("DelMqttHandler: POST %s" % self.request.uri)  # DEBUG
        print("DelMqttHandler: body: %s" % repr(self.request.body))  # DEBUG

        try:
            # Convert posted data from JSON
            data = tornado.escape.json_decode(self.request.body)

            # Parse fields
            conn_id = data["conn_id"]

            # Delete connection
            connections_list.delete(conn_id)

            # Send a WebSocket event to tell that the connection
            # settings have changed
            send_ws_event("connections_list_change")
        except:
            raise tornado.web.HTTPError(400)  # 400 Bad Request

        resp = {"st": "ok"}

        # Produce response as JSON
        print("DelMqttHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class OpenMqttHandler(BaseHandler):
    def post(self):
        global connections_list
        global active_conn_id
        global mqtt_conn

        print("OpenMqttHandler: POST %s" % self.request.uri)  # DEBUG
        print("OpenMqttHandler: body: %s" % repr(self.request.body))  # DEBUG

        # Open a saved MQTT connection
        try:
            # Convert posted data from JSON
            data = tornado.escape.json_decode(self.request.body)

            # Parse fields
            conn_id = data["conn_id"]

            # Load MQTT connection settings from a list of previous connections
            conn = connections_list.get(conn_id)

            # Set active connection
            active_conn_id = conn_id
        except:
            raise tornado.web.HTTPError(400)  # 400 Bad Request

        if not mqtt_conn:
            # Open MQTT connection
            mqtt_conn = mqtt_connection.MqttConnection(
                conn.host, conn.port, conn.username, conn.password, conn.use_tls
            )
        else:
            # Error, MQTT connection already open
            active_conn_id = None
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        # TODO: Refactor MQTT connection opening to a function

        resp = {"st": "ok"}

        # Produce response as JSON
        print("OpenMqttHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class CloseMqttHandler(BaseHandler):
    def post(self):
        global active_conn_id
        global mqtt_conn

        print("CloseMqttHandler: POST %s" % self.request.uri)  # DEBUG
        print("CloseMqttHandler: body: %s" % repr(self.request.body))  # DEBUG

        # Clear active connection
        active_conn_id = None

        if mqtt_conn:
            mqtt_conn.close()
            mqtt_conn = None
        else:
            # Error, MQTT connection not open
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        resp = {"st": "ok"}

        # Produce response as JSON
        print("CloseMqttHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class GetGwsSinksHandler(BaseHandler):
    def get(self):
        global mqtt_conn

        print("GetGwsSinksHandler: GET %s" % self.request.uri)  # DEBUG
        print("GetGwsSinksHandler: body: %s" % repr(self.request.body))  # DEBUG

        if not mqtt_conn:
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        # List all gateways connected to an MQTT broker
        # and all sinks under those gateways
        resp = {"st": "ok", "gws": []}
        for gw_id in mqtt_conn.get_gateways():
            sinks = [s.to_dict() for s in mqtt_conn.get_sinks(gw_id)]
            gw = {"gw_id": gw_id, "sinks": sinks}
            resp["gws"].append(gw)

        # Produce response as JSON
        print("GetGwsSinksHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class GetGwsHandler(BaseHandler):
    def get(self):
        global mqtt_conn

        print("GetGwsHandler: GET %s" % self.request.uri)  # DEBUG
        print("GetGwsHandler: body: %s" % repr(self.request.body))  # DEBUG

        if not mqtt_conn:
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        # List gateways connected to an MQTT broker
        resp = {"st": "ok", "gws": mqtt_conn.get_gateways()}

        # Produce response as JSON
        print("GetGwsHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class GetSinksHandler(BaseHandler):
    def get(self):
        global mqtt_conn

        print("GetSinksHandler: GET %s" % self.request.uri)  # DEBUG
        print("GetSinksHandler: body: %s" % repr(self.request.body))  # DEBUG

        if not mqtt_conn:
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        gw = self.get_arguments("gw")
        if len(gw) != 1:
            # Allow only one "gw" parameter in URL
            raise tornado.web.HTTPError(400)  # 400 Bad Request
        gw = gw[0]

        try:
            # List sinks under a single gateway
            sinks = [s.to_dict() for s in mqtt_conn.get_sinks(gw)]
            resp = {"st": "ok", "sinks": sinks}
        except KeyError:
            raise tornado.web.HTTPError(404)  # 404 Not Found

        # Produce response as JSON
        print("GetSinksHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class ConfigureSinksHandler(BaseHandler):
    def post(self):
        global mqtt_conn

        print("ConfigureSinksHandler: POST %s" % self.request.uri)  # DEBUG
        print("ConfigureSinksHandler: body: %s" % repr(self.request.body))  # DEBUG

        try:
            # Convert posted data from JSON
            data = tornado.escape.json_decode(self.request.body)

            # Parse fields
            gws = data["gws"]

            for gw in gws:
                sinks = []
                for index in range(len(gws[gw])):
                    if gws[gw][index] is None:
                        # Not configuring this index
                        sinks.append(None)
                        continue

                    # Parse sink definition
                    sinks.append(mqtt_connection.Sink(gws[gw][index]))
                gws[gw] = sinks
        except (ValueError, KeyError):
            raise tornado.web.HTTPError(400)  # 400 Bad Request

        if not mqtt_conn:
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        # Configure sinks
        for gw in gws:
            for index in range(len(gws[gw])):
                for sink in gws[gw][index]:
                    try:
                        mqtt_conn.configure_sink(gw, sink)
                    except:
                        # TODO: Handle configuration errors
                        pass

        resp = {"st": "ok"}

        # Produce response as JSON
        print("ConfigureSinksHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class ConfigureSinkHandler(BaseHandler):
    def post(self):
        global mqtt_conn

        print("ConfigureSinkHandler: POST %s" % self.request.uri)  # DEBUG
        print("ConfigureSinkHandler: body: %s" % repr(self.request.body))  # DEBUG

        try:
            # Convert posted data from JSON
            data = tornado.escape.json_decode(self.request.body)

            # Parse fields
            gw_id = data["gw_id"]
            sink_id = data["sink_id"]

            # Parse sink definition
            config = mqtt_connection.Sink(gw_id, sink_id, data["config"])
        except (ValueError, KeyError):
            raise tornado.web.HTTPError(400)  # 400 Bad Request

        if not mqtt_conn:
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        # Configure sink
        try:
            mqtt_conn.configure_sink(gw_id, sink_id, config)
        except:
            # TODO: Handle configuration errors
            pass

        resp = {"st": "ok"}

        # Produce response as JSON
        print("ConfigureSinkHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


class SendDataHandler(BaseHandler):
    def post(self):
        global mqtt_conn

        print("SendDataHandler: POST %s" % self.request.uri)  # DEBUG
        print("SendDataHandler: body: %s" % repr(self.request.body))  # DEBUG

        try:
            # Convert posted data from JSON
            data = tornado.escape.json_decode(self.request.body)

            # Parse fields
            payload = parse_payload(data.get("type", "hex"), data["payload"])
            addr = data.get("addr", "").strip().lower()
            if addr in ("", "all", "broadcast"):
                addr = 0xFFFFFFFF
            elif addr in ("sink", "anysink"):
                addr = 0x00000000
            else:
                addr = int(addr, 0)
            src_ep = data.get("src_ep")
            src_ep = src_ep and int(src_ep, 0) or 0
            dest_ep = data.get("dest_ep")
            dest_ep = dest_ep and int(dest_ep, 0) or 0
            qos = mqtt_connection.Qos(data.get("qos") or "normal")
            init_delay_ms = data.get("init_delay_ms")
            init_delay_ms = init_delay_ms and int(init_delay_ms, 0) or 0
        except (ValueError, KeyError):
            raise tornado.web.HTTPError(400)  # 400 Bad Request

        if not mqtt_conn:
            raise tornado.web.HTTPError(403)  # 403 Forbidden

        # TODO
        try:
            mqtt_conn.send_data(payload, addr, src_ep, dest_ep, qos, init_delay_ms)
        except ValueError:
            raise tornado.web.HTTPError(400)  # 400 Bad Request

        send_ws_data_event("tx", payload, addr, src_ep, dest_ep, 0.0, qos)

        resp = {"st": "ok"}

        # Produce response as JSON
        print("SendDataHandler: response: %s" % repr(resp))  # DEBUG
        self.write(resp)


def parse_payload(type_, payload):
    type_ = type_.lower()
    if type_ not in ("hex", "text"):
        raise ValueError("invalid payload type: '%s'" % type_)

    bytes_ = []

    if type_ == "hex":
        # Hexadecimal data, possibly delimited with commas or spaces
        payload = payload.replace(",", " ")
        payload = payload.split()

        for run in payload:
            if len(run) == 0:
                continue
            elif run[:2] in ("0x", "0X"):
                # One or two hex digits prefixed with "0x"
                if len(run) not in (3, 4):
                    raise ValueError("prefix only supported for 8-bit data: '%s'" % run)
                bytes_.append(int(run[2:], 16))
            elif len(run) <= 2:
                # One or two hex digits
                bytes_.append(int(run, 16))
            elif len(run) % 2 == 0:
                # Even number of consecutive hex digits
                for n in range(0, len(run), 2):
                    bytes_.append(int(run[n : n + 2], 16))
            else:
                raise ValueError("invalid hex data: '%s'" % run)
    else:
        # Text in UTF-8 encoding
        bytes_ = payload.encode("utf-8")

    return bytearray(bytes_)


def to_hex_line(offset, bytes_):
    num_bytes = len(bytes_)
    hex_values = " ".join(
        ["%s%02x" % ((n % 4 == 0) and " " or "", bytes_[n]) for n in range(num_bytes)]
    )
    ascii_values = "".join([(b >= 32 and b < 127) and chr(b) or "." for b in bytes_])

    return "%04x  %-51s   '%s'" % (offset, hex_values, ascii_values)


def send_ws_event(event):
    """Send an event over the WebSocket connection"""

    global tornado_websocket

    # Send data to all connected UIs
    for ws in tornado_websocket.keys():
        print("WebSocket: write: %s" % repr(event))  # DEBUG
        ws.write_message(tornado.escape.json_encode(event))


def send_ws_data_event(
    type_, payload, addr, src_ep=0, dest_ep=0, travel_time=0.0, qos=None
):
    """Send an event that gets printed on the GUI, over the WebSocket connection"""

    global tornado_websocket

    if len(tornado_websocket) == 0:
        # No UIs connected, nothing to do
        return

    if payload is None:
        # DEBUG: Generate random "received" data
        num_bytes = random.randrange(1, 103)
        bytes_ = bytearray(num_bytes)
        for n in range(num_bytes):
            bytes_[n] = random.randrange(0, 256)
    else:
        bytes_ = payload

    if addr == 0x00000000:
        addr_rx_text = "sink"
        addr_tx_text = "to sink"
    elif addr == 0xFFFFFFFF:
        addr_rx_text = "broadcast"
        addr_tx_text = "broadcast"
    else:
        addr_rx_text = "%d" % addr
        addr_tx_text = "to %d" % addr

    text = []
    for b in bytes_:
        text.append("%02x" % b)
    text = " ".join(text)

    if qos is None:
        qos = mqtt_connection.Qos(mqtt_connection.Qos.NORMAL)
    qos_text = str(qos)

    if type_ == "rx":
        # 2021-05-12 00:00:00 Received 102 bytes from 1234567890, ep 123 / 231, travel time 999.999 s
        title_text = (
            "Received %d bytes from %s, ep %d / %d, "
            "travel time: %.3f s, QoS: %s"
            % (len(bytes_), addr_rx_text, src_ep, dest_ep, travel_time, qos_text)
        )
    elif type_ == "tx":
        title_text = "Sending %d bytes %s, ep %d / %d, QoS: %s" % (
            len(bytes_),
            addr_tx_text,
            src_ep,
            dest_ep,
            qos_text,
        )

    message = {
        "type": type_,
        "title": title_text,
        "text": text,
        "mono_text": "",  # Not used
    }

    send_ws_event(message)


def periodic_callback(*args, **kwargs):
    global mqtt_conn

    # Periodically read received data packets from MQTT connection
    if mqtt_conn:
        while True:
            data = mqtt_conn.get_next_rx_data()
            if not data:
                break
            payload = data.data_payload
            addr = data.source_address
            src_ep = data.source_endpoint
            dest_ep = data.destination_endpoint
            travel_time = data.travel_time_ms / 1000.0
            qos = mqtt_connection.Qos(data.qos)
            send_ws_data_event("rx", payload, addr, src_ep, dest_ep, travel_time, qos)


def create_server(port, resource_path, config_db_path, ready_lock):
    global connections_list
    global active_conn_id
    global mqtt_conn

    print("Backend serving on http://localhost:%d" % port)  # DEBUG

    tornado_settings = {
        "static_path": os.path.join(resource_path, "static"),
        "template_path": os.path.join(resource_path, "templates"),
        "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",  # TODO
        "xsrf_cookies": False,  # DEBUG
        "websocket_ping_interval": 20,
        # "login_url": "/login",
    }

    # Use SQLite3 database file for storing the list of connections
    connections_list = settings.MqttConnections(config_db_path)

    try:
        # Try to load connections from an SQLite3 database file
        connections_list.load()
    except settings.Error:
        # Could not access database file, store in RAM only
        pass

    # No open MQTT connection on startup
    active_conn_id = None
    mqtt_conn = None

    # Create a Tornado app
    app = tornado.web.Application(
        [
            # Redirect "/" and "/index.html" to the web app entry point
            tornado.web.url(
                r"/$|/index.html$",
                tornado.web.RedirectHandler,
                dict(url="static/index.html"),
            ),
            # Files generated by the Tornado template engine
            (r"/templates/", MainHandler),
            # HTTP API
            # (r"/api/login", LoginHandler), # TODO
            (r"/api/startup", StartupHandler),
            (r"/api/list-mqtt", ListMqttHandler),
            (r"/api/get-mqtt", GetMqttHandler),
            (r"/api/add-mqtt", AddMqttHandler),
            (r"/api/del-mqtt", DelMqttHandler),
            (r"/api/open-mqtt", OpenMqttHandler),
            (r"/api/close-mqtt", CloseMqttHandler),
            (r"/api/get-gws-sinks", GetGwsSinksHandler),
            (r"/api/get-gws", GetGwsHandler),
            (r"/api/get-sinks", GetSinksHandler),
            (r"/api/configure-sinks", ConfigureSinksHandler),
            (r"/api/configure-sink", ConfigureSinkHandler),
            (r"/api/send-data", SendDataHandler),
            # Websocket API
            (r"/api/websocket", WebSocketHandler),
        ],
        **tornado_settings,
    )

    # Only accept local connections
    app.listen(port, "localhost")

    # Add a periodic callback to the Tornado IO loop
    cb = tornado.ioloop.PeriodicCallback(periodic_callback, 250.0)
    cb.start()

    # Signal caller that the backend is ready
    ready_lock.ready()

    # Start Tornado IO loop
    tornado.ioloop.IOLoop.current().start()

    print("Backend closed")  # DEBUG
