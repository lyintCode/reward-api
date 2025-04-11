import os
import sys
import psycopg2

from dotenv import load_dotenv

load_dotenv()

def check_db() -> bool:
    """
    Функция проверки состояния БД
    Используется при разворачивании контейнера api
    """
    try:
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")  
        db_port = os.getenv("DB_PORT")  

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            connect_timeout=5  
        )
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return False

if __name__ == "__main__":
    if check_db():
        sys.exit(0)  
    else:
        sys.exit(1)  