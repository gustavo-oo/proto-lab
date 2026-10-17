#!/usr/bin/env python3
"""Optional local static server for proto-lab output.

The generated HTML opens fine via ``file://``; this is a thin
``http.server`` wrapper for the moments when a real origin is handier
(relative fetches, devtools, no file:// quirks). Caching is disabled so
regenerated files always show up on reload.

Usage:
    python3 scripts/serve.py [--port 8765] [--dir PATH]

Stdlib only, Python >= 3.8.
"""

import argparse
import functools
import http.server
import os
import sys

DEFAULT_PORT = 8765
DEFAULT_HOST = "127.0.0.1"


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """Static file handler that tells clients never to cache."""

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Serve a proto-lab directory over HTTP with caching disabled "
            "(optional alternative to opening the HTML via file://)."
        )
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="port to listen on (default: %(default)s; 0 picks a free port)",
    )
    parser.add_argument(
        "--dir",
        dest="directory",
        default=None,
        metavar="PATH",
        help="directory to serve (default: current directory)",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    directory = os.path.abspath(args.directory or os.getcwd())
    if not os.path.isdir(directory):
        parser.error("--dir is not a directory: %s" % directory)

    handler = functools.partial(NoCacheHandler, directory=directory)
    with http.server.ThreadingHTTPServer(
        (DEFAULT_HOST, args.port), handler
    ) as server:
        host, port = server.server_address[:2]
        print(
            "Serving %s at http://%s:%d/ (Ctrl+C to stop)" % (directory, host, port),
            flush=True,
        )
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
