from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from urllib.parse import unquote, urlparse, parse_qs
from converter.converter import CurrencyConverter

class SwaggerRequestHandler(BaseHTTPRequestHandler):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(unquote(self.path))
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if path == "/":
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file_path = os.path.join(self.BASE_DIR, "docs", "index.html")
            with open(file_path, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))

        elif path == "/api-docs":
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file_path = os.path.join(self.BASE_DIR, "docs", "swagger_ui.html")
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read().replace("{{spec_url}}", "/docs/swagger.yaml")
                self.wfile.write(html.encode("utf-8"))

        elif path == "/currencies":
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            with CurrencyConverter() as converter:
                currencies = converter.get_currencies()
            self.wfile.write(json.dumps(currencies).encode("utf-8"))

        elif path.startswith("/currencies/"):
            parts = path.strip("/").split("/")
            if len(parts) == 3:
                _, from_currency, to_currency = parts
                try:
                    amount_str = query.get("amount", [None])[0]
                    if amount_str is None:
                        raise ValueError("Параметр amount обязателен")
                    amount = float(amount_str)
                    date = query.get("date", [None])[0]
                    with CurrencyConverter() as converter:
                        result = converter.convert(from_currency, to_currency, amount, date)
                    response = {
                        "from": from_currency,
                        "to": to_currency,
                        "amount": amount,
                        "result": round(result, 2),
                        "date": date or "latest"
                    }
                    self.send_response(200)
                    self._set_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode("utf-8"))
                except Exception as e:
                    print(f"Ошибка при обработке запроса /currencies/: {e}")
                    self.send_response(400)
                    self._set_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    error_msg = {"error": f"Ошибка: {str(e)}. Проверьте корректность параметров, возможно отсутствуют данные по дате."}
                    self.wfile.write(json.dumps(error_msg).encode("utf-8"))
            else:
                self.send_error(404, "Invalid currency conversion path.")

        elif path == "/available-dates":
            try:
                with CurrencyConverter() as converter:
                    dates = converter.get_available_dates()
                self.send_response(200)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(dates).encode("utf-8"))
            except Exception as e:
                print(f"Ошибка при обработке запроса /available-dates: {e}")
                self.send_response(500)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                error_msg = {"error": "Внутренняя ошибка сервера при получении доступных дат."}
                self.wfile.write(json.dumps(error_msg).encode("utf-8"))

        elif path == "/favicon.ico":
            file_path = os.path.join(self.BASE_DIR, "docs", "favicon.ico")
            self._serve_file(file_path, content_type="image/x-icon")

        elif path.startswith("/docs/"):
            file_path = os.path.join(self.BASE_DIR, path.lstrip("/"))
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
                elif file_path.endswith(".ico"):
                    self.send_header("Content-Type", "image/x-icon")
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

    def _serve_file(self, file_path, content_type="text/plain"):
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", content_type)
            self.end_headers()
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, f"{file_path} not found.")

def run(server_class=HTTPServer, handler_class=SwaggerRequestHandler):
    port = int(os.environ.get("PORT", 8000))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Swagger UI available at http://localhost:{port}/api-docs")
    print(f"Index page available at http://localhost:{port}/")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
