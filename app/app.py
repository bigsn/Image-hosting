from http.server import HTTPServer, BaseHTTPRequestHandler
from loguru import logger

logger.add("../logs/app.log")

logger.info("Это сообщение попадет и в консоль, и в файл my_app.log")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f'Get query {self.path}')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = f'<h1>Hello, World!</h1>'
        self.wfile.write(message.encode('utf-8'))


# Конфигурация сервера
host = 'localhost'
port = 8000

# Запуск сервера
server = HTTPServer((host, port), SimpleHandler)
logger.info(f"Сервер запущен на http://{host}:{port}")

try:
    server.serve_forever()
except KeyboardInterrupt as e:
    logger.error(f'ошибка сервера {e}')

finally:
    server.server_close()
    logger.info("Сервер остановлен")

