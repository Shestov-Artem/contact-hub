import os
import psycopg2
from dotenv import load_dotenv # Загружаем параметры БД
from django.contrib.auth.hashers import make_password, check_password # Хэширование паролей

# Загружаем переменные окружения
load_dotenv()

def get_db_connection():
    """Устанавливает соединение с PostgreSQL"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def ensure_users_table_exists():
    """Создает таблицу users, если она не существует"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(128) NOT NULL
                )
            """)
            conn.commit()
            print("Таблица users готова к работе")
    except Exception as e:
        print(f"Ошибка при создании таблицы users: {e}")
    finally:
        if conn:
            conn.close()

def create_user(username, password):
    """
    Создает нового пользователя с хешированным паролем
    :param username: Логин пользователя
    :param password: Пароль в открытом виде
    :return: ID созданного пользователя или None
    """
    conn = None
    try:
        hashed_password = make_password(password)
        
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
                RETURNING id
                """,
                (username, hashed_password)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            return user_id
    except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")
        return None
    finally:
        if conn:
            conn.close()

def find_user_by_credentials(username, password):
    """
    Проверяет учетные данные пользователя
    :param username: Логин пользователя
    :param password: Пароль в открытом виде
    :return: ID пользователя или None
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, password FROM users 
                WHERE username = %s
                """,
                (username,)
            )
            user_data = cursor.fetchone()
            
            if user_data:
                user_id, hashed_password = user_data
                if check_password(password, hashed_password):
                    return user_id
        return None
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return None
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Проверяем/создаем таблицу при запуске
    ensure_users_table_exists()
    
    # Тестовый пример использования
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    
    user_id = find_user_by_credentials(username, password)
    
    if user_id:
        print(f"Успешный вход! ID пользователя: {user_id}")
    else:
        print("Пользователь не найден, создаем нового...")
        new_user_id = create_user(username, password)
        if new_user_id:
            print(f"Пользователь создан с ID: {new_user_id}")
            print("Попробуйте войти снова")
        else:
            print("Не удалось создать пользователя")