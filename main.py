from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time

hostName = "127.0.0.1"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Указываем путь к файлу contacts.html
        file_path = 'contacts.html'

        try:
            # Проверяем существование файла
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                # Читаем и отправляем содержимое файла
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("File not found", "utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"Server error: {str(e)}", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")