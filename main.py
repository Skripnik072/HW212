from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mimetypes

# Настройки сервера
hostName = "127.0.0.1"  # Хост для подключения
serverPort = 8080  # Порт сервера

# Словарь соответствий расширений файлов и MIME-типов
content_types = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.json': 'application/json',
    '.pdf': 'application/pdf'
}


class MyServer(BaseHTTPRequestHandler):
    """
    Обработчик HTTP-запросов с поддержкой статических файлов
    """

    def do_GET(self):
        # По умолчанию открываем contacts.html по условию ДЗ
        if self.path == '/':
            self.path = '/contacts.html'

        # Получаем абсолютный путь к запрашиваемому файлу
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, self.path[1:])  # Убираем начальный слеш

        # Проверяем существование файла
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            self.send_error(404, "Файл не найден")
            return

        # Получаем расширение файла
        file_ext = os.path.splitext(file_path)[1].lower()

        # Определяем MIME-тип файла из нашего словаря
        mime_type = content_types.get(file_ext)
        if mime_type is None:
            # Если расширение неизвестно, используем стандартное определение
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'  # Тип по умолчанию

        try:
            with open(file_path, 'rb') as file:
                # Отправляем успешный ответ
                self.send_response(200)
                self.send_header("Content-type", mime_type)
                self.send_header("Content-Length", str(os.path.getsize(file_path)))
                self.end_headers()

                # Отправляем файл частями для оптимизации памяти
                while True:
                    data = file.read(1024)  # Читаем по 1 КБ за раз
                    if not data:
                        break
                    self.wfile.write(data)

        except Exception as e:
            self.send_error(500, f"Ошибка сервера: {str(e)}")


if __name__ == "__main__":
    # Инициализируем систему MIME-типов для неизвестных расширений
    mimetypes.init()

    # Создаем и запускаем сервер
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен по адресу http://{hostName}:{serverPort}")

    try:
        print("Сервер готов к работе...")
        webServer.serve_forever()  # Запускаем бесконечный цикл обработки запросов
    except KeyboardInterrupt:
        print("\nПолучен сигнал прерывания...")
        pass

    webServer.server_close()
    print("Сервер остановлен.")