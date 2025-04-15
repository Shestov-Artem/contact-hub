import psycopg2

host = "localhost"
port = "6432"  
database = "postgres"  
db_user = "postgres"
db_password = "3507874"

connection = None
cursor = None

def find_user_by_credentials(username, password):
    global connection, cursor
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user = db_user,
            password = db_password,
        )
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username = %s AND password = %s", (username, password)
        )

        user = cursor.fetchone()

        if user:
            return user[0] 
        else:
            return None  

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL:", _ex)
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# тест использование
username = input( "имя пользователя: ")
password = input(" пароль: ")

user_id = find_user_by_credentials(username, password)

if user_id:
    print(f"Пользователь найден - ID: {user_id}")
else:
    print("Пользователь не найден")