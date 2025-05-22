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

    def test_currency_list(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        conn.request("GET", "/currencies")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode())
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        conn.close()

    def test_valid_conversion(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        conn.request("GET", "/currencies/USD/EUR?amount=100")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode())
        self.assertIn("result", data)
        self.assertEqual(data["from"], "USD")
        self.assertEqual(data["to"], "EUR")
        self.assertAlmostEqual(data["amount"], 100)
        conn.close()

    def test_invalid_conversion_path(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        conn.request("GET", "/currencies/USD?amount=100")
        response = conn.getresponse()
        self.assertEqual(response.status, 404)
        conn.close()

    def test_invalid_amount(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        conn.request("GET", "/currencies/USD/EUR?amount=abc")
        response = conn.getresponse()
        self.assertEqual(response.status, 400)
        data = json.loads(response.read().decode())
        self.assertIn("error", data)
        conn.close()

    def test_not_found(self):
        conn = http.client.HTTPConnection("localhost", 8081)
        conn.request("GET", "/invalid")
        response = conn.getresponse()
        self.assertEqual(response.status, 404)
        conn.close()

if __name__ == '__main__':
    unittest.main()
