import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from app import Handler


class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}") as response:
            return response.status, json.load(response)

    def test_root(self):
        status, payload = self.get("/")
        self.assertEqual(status, 200)
        self.assertEqual(payload["message"], "Hello, World!")
        self.assertEqual(payload["port"], 32777)

    def test_health(self):
        status, payload = self.get("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"status": "ok"})

    def test_not_found(self):
        with self.assertRaises(urllib.error.HTTPError) as context:
            self.get("/missing")
        self.assertEqual(context.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
