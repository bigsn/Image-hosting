from database import save_metadata
from conf import FILE_EXTENSION, MAX_FILE_SIZE
from pathlib import Path
from uuid import uuid4
from loguru import logger
import datetime
import os


def is_allowed(filename):
    return Path(filename).suffix in FILE_EXTENSION

# валидация данных
def validate(filename, data):
    if not is_allowed(filename):
        return False
    if data == 0 or len(data) > MAX_FILE_SIZE:
        return False
    return True

# получить имя файла из multipart/form-data
def get_name(post_data):
    boundary = post_data.split(b'\r\n')[0]
    part = post_data.split(boundary)[1].split(b'\r\n')[1].decode("utf-8")
    for i in part.split(';'):
        i = i.strip()
        if i.startswith("filename="):
            i = i.lstrip("filename=")
            filename = i.strip('"')
            logger.info(f'file_name: {filename}')
            return filename
    return "1.txt"

# получить данные из multipart/form-data
def get_data(post_data):
    boundary = post_data.split(b'\r\n')[0]
    c = post_data.split(boundary)[1].split(b'\r\n', 2)[2]
    if c.startswith(b'Content-Type:'):
        data = c.split(b'\r\n\r\n', 1)[1]
        return data[:-2]
    return 0

# запись в базу данных и в файл
def save_image(post_data):
    filename = get_name(post_data)
    data = get_data(post_data)

    if validate(filename, data):
        file_name = Path(filename).stem
        file_ext = Path(filename).suffix
        origin_file_name = f'{file_name}_{str(uuid4())[:8]}.{file_ext}'
        try:
            save_metadata(file_name, origin_file_name, int(len(data) / 1024), file_ext)
            with open(f'./images/{origin_file_name}', "wb") as f:
                f.write(data)
        except:
            logger.exception("filed saved to database")
            return None
        return  origin_file_name
    return None

# создание файла бекапа
def backup(images):
    date = datetime.datetime.now().strftime('%Y%m%d')
    try:
        f = open(f'./backup/backup_{date}.sql', 'w')
        for row in images:
            f.write(f'INSERT INTO images (filename, original_name, size, upload_time, file_type) VALUES {row[1:]};/n')
    except :
        logger.exception("backup filed")

# удаление файла
def delete_file(filename):
    file_path = f'./images/{filename}'
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"File '{file_path}' has been deleted.")
    else:
        logger.error(f"File '{file_path}' does not exist.")
