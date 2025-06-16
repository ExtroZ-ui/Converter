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

    def _get_conn(self):
        return http.client.HTTPConnection(self.server_address[0], self.server_address[1])

    def test_docs_page(self):
        conn = self._get_conn()
        conn.request("GET", "/api-docs")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        html = response.read().decode()
        self.assertIn("<title>", html)
        conn.close()

    def test_currency_list(self):
        conn = self._get_conn()
        conn.request("GET", "/currencies")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode())
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        conn.close()

    def test_valid_conversion(self):
        conn = self._get_conn()
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
        conn = self._get_conn()
        conn.request("GET", "/currencies/USD?amount=100")
        response = conn.getresponse()
        self.assertEqual(response.status, 404)
        conn.close()

    def test_invalid_amount(self):
        conn = self._get_conn()
        conn.request("GET", "/currencies/USD/EUR?amount=abc")
        response = conn.getresponse()
        self.assertEqual(response.status, 400)
        data = json.loads(response.read().decode())
        self.assertIn("error", data)
        conn.close()

    def test_not_found(self):
        conn = self._get_conn()
        conn.request("GET", "/invalid")
        response = conn.getresponse()
        self.assertEqual(response.status, 404)
        conn.close()

    def test_available_dates(self):
        conn = self._get_conn()
        conn.request("GET", "/available-dates")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode())
        self.assertIsInstance(data, list)
        # Даты должны быть строками в формате YYYY-MM-DD
        for d in data:
            self.assertIsInstance(d, str)
            self.assertRegex(d, r"\d{4}-\d{2}-\d{2}")
        conn.close()

if __name__ == '__main__':
    unittest.main()
