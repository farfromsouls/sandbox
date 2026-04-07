from mysql.connector import connect, Error

import os


def get_connection():
    connection = connect(
        host=os.getenv('DB_HOST', 'mysql'),
        user=os.getenv('DB_USER', 'myuser'),
        password=os.getenv('DB_PASSWORD', 'mypassword'),
        database=os.getenv('DB_NAME', 'mydb')
    )
    # Не ловлю ошибки т.к. всеравно в docker-compose есть health-check
    return connection

def main():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE users (id INT, name VARCHAR(100))")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    cursor.execute("INSERT INTO users VALUES (2, 'Bob')")
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)
    
if __name__ == "__main__":
    main()
    

