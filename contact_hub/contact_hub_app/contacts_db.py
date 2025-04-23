import os
import psycopg2
from dotenv import load_dotenv  # Загружаем параметры БД

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

def ensure_tables_exist():
    """Создает таблицу contacts, если она не существуют"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            
            # Создаем таблицу contacts, если она не существует
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL,
                    photo_url VARCHAR(255),
                    email VARCHAR(100),
                    description TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()
            print("Таблицаcontacts готова к работе")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Проверяем/создаем таблицы при запуске
    ensure_tables_exist()
    print("Инициализация базы данных завершена")