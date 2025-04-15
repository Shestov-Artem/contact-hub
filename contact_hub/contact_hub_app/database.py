import psycopg2

host = "localhost"
port = "6432"  
database = "postgres"  
user = "postgres"
password = "3507874"


try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
    )

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * from users"
        )
        print(cursor.fetchone())


   
except Exception as _ex:
    print("[INFO] Erorr while working with PostgreSQL", _ex)

finally:
    if connection:
        connection.close()
        print("[INFO] connection close")