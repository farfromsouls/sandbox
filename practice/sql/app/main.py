from mysql.connector import connect
import os
import sqlparse

import subprocess



class Database():
    def __init__(self) -> None:
        self.host=os.getenv('DB_HOST', 'mysql')
        self.user=os.getenv('DB_ROOT_USER', 'root')     
        self.password=os.getenv('MYSQL_ROOT_PASSWORD', 'root_password')  
        
        self.connection = self.__get_connection()  
        self.cursor = self.connection.cursor()
    
    def __get_connection(self):
        connection = connect(
            host=self.host,
            user=self.user,         
            password=self.password  
        )
        return connection

    def __fetchall(self):
        print(self.cursor.fetchall())
        
    def __exec(self, command):
        cmd = command.strip()
        if cmd.endswith(';'):
            cmd = cmd[:-1].strip()
        if cmd:
            self.cursor.execute(cmd)
            
    def run_cli(self, script):
        script_path = f"/app/sql_scripts/{script}.sql"
        host=self.host
        user=self.user         
        password=self.password  
        
        cmd = [
            'mysql',
            f'-h{host}',
            f'-u{user}',
            f'-p{password}',
            '--ssl=0',
            '-e', f'source {script_path}'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Ошибка выполнения {script}:")
            print(result.stderr)
            raise Exception(f"Скрипт {script} завершился с ошибкой")
        else:
            print(f"Скрипт {script} выполнен успешно")
            if result.stdout:
                print(result.stdout)

    def run(self, script):
        script_path = f"/app/sql_scripts/{script}.sql"
        with open(script_path, "r", encoding="utf-8") as f:
            statements = sqlparse.split(f.read())
        
        for stmt in statements:
            clean_stmt = stmt.strip()
            if clean_stmt.endswith(';'):
                clean_stmt = clean_stmt[:-1].strip()
            if clean_stmt:
                self.__exec(clean_stmt)
                if clean_stmt.upper().startswith("SELECT"):
                    self.__fetchall()

if __name__ == "__main__":
    test = Database()
    # test.run_cli("sakila-schema")
    # test.run_cli("sakila-data")    
    # test.run("sakila") 
    
    test.run("fav_food")