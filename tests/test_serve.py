"""Tests for scripts/serve.py — the optional local static server.

The server is started as a real child process on a free port over a
temporary directory, exercised over HTTP with urllib, and always stopped
(with a 10s grace period) so the suite never leaves a process or port
behind.
"""

import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVE_SCRIPT = REPO_ROOT / "scripts" / "serve.py"

HOST = "127.0.0.1"
START_TIMEOUT = 10.0
SHUTDOWN_TIMEOUT = 10.0
INDEX_BODY = "<!doctype html>\n<html><body><h1>proto-lab serve</h1></body></html>\n"


def free_port():
    """Return an unused TCP port on the loopback interface."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return sock.getsockname()[1]


def wait_for_server(proc, port, timeout=START_TIMEOUT):
    """Wait until the server accepts connections; fail fast if it dies."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise AssertionError(
                "serve.py exited with code %s before accepting connections:\n%s"
                % (proc.returncode, proc.stderr.read().decode("utf-8", "replace"))
            )
        try:
            with socket.create_connection((HOST, port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.05)
    raise AssertionError("serve.py did not accept connections within %.0fs" % timeout)


def stop_process(proc, timeout=SHUTDOWN_TIMEOUT):
    """Terminate a child process, escalating to SIGKILL if it lingers."""
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=timeout)


class ServeScriptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.mkdtemp(prefix="proto-lab-serve-")
        (Path(cls.tmpdir) / "index.html").write_text(INDEX_BODY, encoding="utf-8")
        cls.port = free_port()
        cls.proc = subprocess.Popen(
            [
                sys.executable,
                str(SERVE_SCRIPT),
                "--port",
                str(cls.port),
                "--dir",
                cls.tmpdir,
            ],
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            wait_for_server(cls.proc, cls.port)
        except BaseException:
            cls._cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls._cleanup()

    @classmethod
    def _cleanup(cls):
        proc = getattr(cls, "proc", None)
        if proc is not None:
            stop_process(proc)
            for stream in (proc.stdout, proc.stderr):
                if stream is not None and not stream.closed:
                    stream.close()
        shutil.rmtree(getattr(cls, "tmpdir", ""), ignore_errors=True)

    def fetch(self, path="/index.html"):
        url = "http://%s:%d%s" % (HOST, self.port, path)
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status, response.headers, response.read()

    def test_serves_index_html_from_directory(self):
        status, _, body = self.fetch("/index.html")

        self.assertEqual(status, 200)
        self.assertEqual(body, INDEX_BODY.encode("utf-8"))

    def test_index_is_the_directory_root(self):
        status, _, body = self.fetch("/")

        self.assertEqual(status, 200)
        self.assertEqual(body, INDEX_BODY.encode("utf-8"))

    def test_disables_caching(self):
        _, headers, _ = self.fetch("/index.html")

        self.assertEqual(headers.get("Cache-Control"), "no-store")


if __name__ == "__main__":
    unittest.main()
