import sys
from http.server import HTTPServer
from database import init_db, save_metadata
from http_handler import SimpleHandler
from loguru import logger
from conf import HOST, PORT

#Настройка логирования
logger.remove()
logger.add("./logs/app.log", level="DEBUG")
logger.add(sys.stderr, level="DEBUG", colorize=True)

# Подключение к базе
init_db()

# Запуск сервера
server = HTTPServer((HOST, PORT), SimpleHandler)
logger.info(f"Сервер запущен на http://{HOST}:{PORT}")
try:
    server.serve_forever()
except KeyboardInterrupt as e:
    logger.exception(f'ошибка сервера')
    raise

finally:
    server.server_close()
    logger.info("Сервер остановлен")

