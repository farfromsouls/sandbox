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

def fetchall(line, cursor):
    print(f"{line}: {cursor.fetchall()}")

def main(script):
    connection = get_connection()
    cursor = connection.cursor()
    exec = cursor.execute
    
    with open(f"{script}.txt", "r", encoding="utf-8") as sql_script_file:

        buffer = ""
        line_command = 1
        line_i = 1
        
        for line in sql_script_file:
            if line != "\n":
                buffer = buffer + line
            
            if line.endswith(';\n') or line.endswith(';'):
                exec(buffer)
                
                if buffer.strip().upper().startswith("SELECT"):
                    fetchall(line_command+1, cursor)
                    
                buffer = ""
                line_command = line_i + 1
                
            line_i += 1
                

if __name__ == "__main__":
    main("fav_food")
    

