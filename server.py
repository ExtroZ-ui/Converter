from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import unquote
from converter.converter import CurrencyConverter
import json

class SwaggerRequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        # Обработка preflight CORS-запроса
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        path = unquote(self.path)

        if path == "/" or path == "/api-docs":
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("swagger/swagger_ui.html", "r", encoding="utf-8") as f:
                html = f.read().replace("{{spec_url}}", "/swagger/swagger.yaml")
                self.wfile.write(html.encode("utf-8"))

        elif path == "/currencies":
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            converter = CurrencyConverter()
            currencies = converter.get_currencies()
            self.wfile.write(json.dumps(currencies).encode('utf-8'))

        elif path.startswith("/swagger/"):
            file_path = "." + path
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                self._set_cors_headers()

                if file_path.endswith(".yaml"):
                    self.send_header("Content-Type", "application/x-yaml")
                elif file_path.endswith(".html"):
                    self.send_header("Content-Type", "text/html")
                elif file_path.endswith(".js"):
                    self.send_header("Content-Type", "application/javascript")
                elif file_path.endswith(".css"):
                    self.send_header("Content-Type", "text/css")
                else:
                    self.send_error(415, "Unsupported file type.")
                    return
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found.")

        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        path = unquote(self.path)

        if path == "/convert":
            content_length = int(self.headers.get('Content-Length', 0))
            content_type = self.headers.get('Content-Type', '')

            if content_type != "application/json":
                self.send_response(400)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'{"error": "Content-Type must be application/json"}')
                return

            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                from_currency = data.get("from")
                to_currency = data.get("to")
                amount = data.get("amount")

                if not all([from_currency, to_currency, isinstance(amount, (int, float))]):
                    raise ValueError("Invalid input: 'from', 'to', and numeric 'amount' are required.")

                converter = CurrencyConverter()
                result = converter.convert(from_currency, to_currency, float(amount))

                response = {
                    "result": round(result, 2),
                    "from": from_currency,
                    "to": to_currency,
                    "amount": amount
                }

                self.send_response(200)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))

            except Exception as e:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        else:
            self.send_error(404, "Not Found")


def run(server_class=HTTPServer, handler_class=SwaggerRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Swagger UI available at http://localhost:{port}/api-docs")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
