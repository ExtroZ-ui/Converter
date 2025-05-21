import unittest
import http.client
import json
import threading
from server import SwaggerRequestHandler, HTTPServer

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8081)
        cls.httpd = HTTPServer(cls.server_address, SwaggerRequestHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join()

    def test_docs_page(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        conn.request("GET", "/api-docs")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        html = response.read().decode()
        self.assertIn("<title>", html)
        conn.close()

    def test_post_convert_valid(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        headers = {'Content-Type': 'application/json'}
        payload = {
            "from": "USD",
            "to": "EUR",
            "amount": 100
        }
        conn.request("POST", "/convert", body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode())
        self.assertIn("result", data)
        conn.close()

    def test_post_convert_invalid_content_type(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        conn.request("POST", "/convert", body="notjson", headers={'Content-Type': 'text/plain'})
        response = conn.getresponse()
        self.assertEqual(response.status, 400)
        conn.close()

    def test_not_found(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        conn.request("GET", "/invalid")
        response = conn.getresponse()
        self.assertEqual(response.status, 404)
        conn.close()

if __name__ == '__main__':
    unittest.main()

