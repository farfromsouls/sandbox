from mysql.connector import connect

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
    exec = cursor.execute
    fetchall = lambda: print(cursor.fetchall())
    
    with open("sql_script.txt", "r", encoding="utf-8") as sql_script_file:
        sql_script_text = sql_script_file.read()
        sql_commands = sql_script_text.split("\n\n")
    
        for command in sql_commands:
            if command != "":
                exec(command)
                if command.startswith("SELECT"):
                    fetchall()

if __name__ == "__main__":
    main()
    

