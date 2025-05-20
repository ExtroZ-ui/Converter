from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import unquote


class SwaggerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(self.path)

        if path == "/" or path == "/docs":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("swagger/swagger-ui.html", "r", encoding="utf-8") as f:
                html = f.read().replace("{{spec_url}}", "/swagger/swagger.yaml")
                self.wfile.write(html.encode("utf-8"))

        elif path.startswith("/swagger/"):
            file_path = "." + path
            if os.path.exists(file_path):
                if file_path.endswith(".yaml"):
                    self.send_response(200)
                    self.send_header("Content-type", "application/x-yaml")
                    self.end_headers()
                    with open(file_path, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(415, "Unsupported file type.")
            else:
                self.send_error(404, "File not found.")
        else:
            self.send_error(404, "Not Found")


def run(server_class=HTTPServer, handler_class=SwaggerRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Swagger UI available at http://localhost:{port}/docs")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
