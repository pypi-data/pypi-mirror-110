#!/usr/bin/env python3

import sys
import os
import random
import multiprocessing as mp

import appdirs

from . import frontend, backend


# Unique app name used in configuration and data file paths
APP_PATH_NAME = "com.wirepas.console"

# Company name used in configuration and data file paths (only on Windows)
COMPANY_PATH_NAME = "Wirepas_Ltd"  # WNT uses this path as well


class ReadyLock:
    """A lock for waiting for a resource to be ready"""

    def __init__(self):
        self.lock = mp.Lock()
        self.lock.acquire()

    def ready(self):
        self.lock.release()

    def wait(self):
        self.lock.acquire()


def main():
    # Allow producing a Windows executable that works
    # correctly with the multiprocessing module
    mp.freeze_support()

    # Always open separate Python interpreters for frontend and backend
    mp.set_start_method("spawn")

    # Select a random port for Tornado web server
    # port = random.randrange(1024, 65536)
    port = 1414  # DEBUG

    # Path for all web resources (Tornado templates, HTML, CSS, JavaScript, SVG, ...)
    resource_path = os.path.join(os.path.dirname(__file__), "resources")

    # Path for all settings databases (list of connections, ...)
    config_db_path = appdirs.user_config_dir(APP_PATH_NAME, COMPANY_PATH_NAME)

    # Create a Lock object for signaling when backend is ready
    be_ready_lock = ReadyLock()

    # TODO: Parse command line arguments
    open_frontend = True
    if "--no-webview" in sys.argv[1:]:
        open_frontend = False

    # Open backend in a new process
    be = mp.Process(
        target=backend.create_server,
        args=(port, resource_path, config_db_path, be_ready_lock),
    )
    be.start()

    # Wait for backend to be ready
    be_ready_lock.wait()

    if open_frontend:
        # Open frontend in a new process
        fe = mp.Process(target=frontend.open_webview_window, args=(port,))
        fe.start()

        # Wait for frontend process to end
        fe.join()

        # Tell backend process to end
        be.terminate()  # TODO: A kinder way to stop the backend process

    # Wait for backebd process to end
    be.join()

    return 0


# Support for multiprocessing by only running main program on the main process
if __name__ == "__main__":
    sys.exit(main())
