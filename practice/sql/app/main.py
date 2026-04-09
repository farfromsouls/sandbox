from mysql.connector import connect

import os


class Database():
    def __init__(self, script: str) -> None:
        self.script = script
        
        self.script_path = f"/app/sql_scripts/{script}.sql" 
        
        self.connection = self.__get_connection()  
        self.cursor = self.connection.cursor()
    
    def __get_connection(self):
        connection = connect(
            host=os.getenv('DB_HOST', 'mysql'),
            user=os.getenv('DB_ROOT_USER', 'root'),         
            password=os.getenv('MYSQL_ROOT_PASSWORD', 'root_password')  
        )
        return connection

    def __fetchall(self, line):
        print(f"{line}: {self.cursor.fetchall()}")
        
    def __exec(self, command):
        self.cursor.execute(command)

    def run(self):
        with open(self.script_path, "r", encoding="utf-8") as sql_script_file:

            buffer = ""
            line_command = 1
            line_i = 1
            
            for line in sql_script_file:
                if line != "\n":
                    buffer = buffer + line
                
                if line.endswith(';\n') or line.endswith(';'):
                    self.__exec(buffer)
                    
                    if buffer.strip().upper().startswith("SELECT"):
                        self.__fetchall(line_command+1)
                        
                    buffer = ""
                    line_command = line_i + 1
                    
                line_i += 1


if __name__ == "__main__":
    test = Database("fav_food")
    test.run()