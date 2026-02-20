import psycopg2
from conf import DB_CONFIG
from loguru import logger

def get_db():
    try:
        db_conn = psycopg2.connect(**DB_CONFIG)
        return db_conn

    except:
        logger.exception(f"Database connection error")



def exec_query(query, log_success, log_fail, params=None, fetch_data=0):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                logger.success(log_success)
                conn.commit()
                if fetch_data == 1:
                    logger.info("fetch query")
                    return cur.fetchall()
    except:
        logger.exception(log_fail)
        raise




def init_db():
    query ="""
        CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            size INTEGER NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_type TEXT NOT NULL
        );    
    """
    log_success = "Tables initialized successfully"
    log_fail = "Failed to initialize table"
    exec_query(query, log_success, log_fail)

def save_metadata(filename, original_name, size, file_type):
    query ="""
        INSERT INTO images (filename, original_name, size, file_type) 
        VALUES (%s,%s, %s, %s);    
    """
    log_success = "Image save successfully"
    log_fail = "Failed to save image"
    params = (filename, original_name, size, file_type)
    exec_query(query, log_success, log_fail, params=params)

def del_image(original_name):
    query ="""
        DELETE FROM images WHERE original_name = %s;    
    """
    log_success = "Image delete"
    log_fail = "Failed to delete image"
    params = (original_name,)
    exec_query(query, log_success, log_fail, params=params)

def get_images(page=1, page_size=10):
    offset = (page - 1) * page_size
    query ="""
        SELECT * FROM images ORDER BY upload_time DESC LIMIT %s OFFSET %s;    
    """
    log_success = "Images get successfully"
    log_fail = "Failed to get images"
    params = (page_size, offset)
    data= exec_query(query, log_success, log_fail, params=params, fetch_data=1)
    return  data

def get_all_images():
    query ="""
        SELECT * FROM images;    
    """
    log_success = "Images get successfully"
    log_fail = "Failed to get images"
    data= exec_query(query, log_success, log_fail, fetch_data=1)
    return  data

def get_count():
    query ="""
        SELECT count(filename) FROM images;    
    """
    log_success = "Images get successfully"
    log_fail = "Failed to get images"
    data= exec_query(query, log_success, log_fail, fetch_data=1)
    return  data

def get_image(original_name):
    query ="""
        SELECT * FROM images WHERE original_name = %s;    
    """
    log_success = "Image get successfully"
    log_fail = "Failed to get image"
    params = (original_name,)
    data = exec_query(query, log_success, log_fail, params=params,fetch_data=1)
    return  data[0]


