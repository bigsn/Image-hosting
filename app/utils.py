from database import save_metadata
from conf import FILE_EXTENSION, MAX_FILE_SIZE
from pathlib import Path
from uuid import uuid4
from loguru import logger
import datetime
import os


def is_allowed(filename):
    return Path(filename).suffix in FILE_EXTENSION

def validate(filename, data):
    if not is_allowed(filename):
        return False
    if len(data) > MAX_FILE_SIZE:
        return False
    return True

def save_image(filename, data):
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

def backup(images):
    date = datetime.datetime.now().strftime('%Y%m%d')
    try:
        f = open(f'./backup/backup_{date}.sql', 'w')
        for row in images:
            f.write(f'INSERT INTO images (filename, original_name, size, upload_time, file_type) VALUES {row};')
    except :
        logger.exception("backup filed")



def delete_file(filename):
    file_path = f'./images/{filename}'
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"File '{file_path}' has been deleted.")
    else:
        logger.error(f"File '{file_path}' does not exist.")
