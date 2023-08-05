#!/usr/bin/env python3

import webview


def open_webview_window(port):
    """Open a WebView GUI"""

    # DEBUG
    print("Opening WebView GUI on http://localhost:%d" % port)

    # Create a new WebView window
    window = webview.create_window(
        "Wirepas Console",
        url="http://localhost:%d/" % port,
        width=800,
        height=800,
        frameless=False,
        easy_drag=False,
        text_select=False,
    )

    # Run WebView GUI
    webview.start(http_server=False)

    # DEBUG
    print("WebView GUI closed")
