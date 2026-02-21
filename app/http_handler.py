import json
from http.server import BaseHTTPRequestHandler
from database import get_images, del_image, get_all_images, get_count
from loguru import logger
from utils import validate, save_image, delete_file, backup
from urllib.parse import urlparse, parse_qs
from math import ceil
import sys

logger.remove()
logger.add("./logs/app.log", level="DEBUG")
logger.add(sys.stderr, level="DEBUG", colorize=True)

class SimpleHandler(BaseHTTPRequestHandler):
#    server_version = "ImageHost/0.1"

    def do_GET(self):
        parsed_path = urlparse(self.path)
        logger.info(f'query: {self.path}')
        page = parse_qs(parsed_path.query).get('page', ['1'])[0]
        page_size= parse_qs(parsed_path.query).get('page_size', ['10'])[0]
        if page.isdigit():
            page = int(page)
        else: page = 1
        if page_size.isdigit():
            page_size = int(page_size)
        else: page_size = 10
        logger.info(f'pages: {page}, {page_size}')
        if parsed_path.path == "/get-images/":
            max_images = get_count()
            logger.info(f'count page: {ceil(max_images[0] / page_size)}')
            images = get_images(page, page_size)
            images = [
                {
                    'filename': i[1],
                    'original_filename': i[2],
                    'size': i[3],
                    'date': i[4].strftime("%Y-%m-%d %H:%M:%S"),
                    'type': i[5]
                }
                for i in images
            ]
            return  self.send_json({"images": images, "max_images": ceil(max_images[0] / page_size)}, 200)

        elif parsed_path.path.startswith("/backup/"):
            images = get_all_images()
            backup(images)
            return self.send_json({"backup": "ok"}, 200)


    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/upload":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                logger.info(int(self.headers.get('Content-Length', 0)))
                return  self.send_json({'error': 'Not file'}, 400)
            filename = self.headers.get('X-Filename', '')
            logger.info(filename)
            if not filename:
                return self.send_json({'error': 'Not file name'}, 400)
            post_data = self.rfile.read(content_length)

            # валидация
            if validate(filename, post_data):
                origin_name = save_image(filename, post_data)
                if origin_name:
                    response = {"status": "success", "message": f'http://localhost/images/{origin_name}'}
                    return self.send_json(response, 200)
                else:
                    return self.send_json({'error': 'Not saved'}, 404)
            else:
                return self.send_json({'error': 'Not saved'}, 404)

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        logger.info(f'DELETE query {parsed_path.path}')

        if parsed_path.path.startswith("/delete/"):
            origin_file_name = parsed_path.path.split("/")[2]
            try:
                del_image(origin_file_name)
                delete_file(origin_file_name)
                self.send_json({"delete": "ok"}, 200)
            except :
                self.send_json({"delete": "false"}, 400)

    def send_json(self, data, status:int):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
