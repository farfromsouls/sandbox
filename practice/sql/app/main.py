from mysql.connector import connect, Error as MySQLError
import os
import sqlparse
import subprocess


class Database:
    def __init__(self) -> None:
        self.host = os.getenv("DB_HOST", "mysql")
        self.user = os.getenv("DB_ROOT_USER", "root")
        self.password = os.getenv("MYSQL_ROOT_PASSWORD", "root_password")

        self.connection = self._get_connection(database=None)
        self.cursor = self.connection.cursor()

    def _get_connection(self, database=None):
        return connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=database,
            autocommit=True,
            use_pure=True,
            charset="utf8mb4",
        )

    def _reconnect(self, database=None):
        self.connection.close()
        self.connection = self._get_connection(database=database)
        self.cursor = self.connection.cursor()

    def use_database(self, db_name: str):
        self.cursor.execute(f"USE {db_name};")
        print(f"🔁 Переключились на базу данных `{db_name}`")

    def run_cli(self, script: str, database: str = None):
        script_path = f"/app/sql_scripts/{script}.sql"

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Файл {script_path} не найден")

        cmd = [
            "mysql",
            f"-h{self.host}",
            f"-u{self.user}",
            f"-p{self.password}",
            "--ssl=0",
        ]

        if database:
            cmd.append(f"--database={database}")

        cmd.extend([
            "--init-command=SET AUTOCOMMIT=1",
            "-e", f"source {script_path}"
        ])

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Ошибка выполнения {script}.sql:")
            print(result.stderr)
            raise RuntimeError(f"Скрипт {script}.sql завершился с ошибкой")
        else:
            print(f"✅ Скрипт {script}.sql выполнен успешно")
            if result.stdout:
                print(result.stdout)

        self._reconnect(database=database)

    def run(self, script: str):
        script_path = f"/app/sql_scripts/{script}.sql"

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Файл {script_path} не найден")

        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        statements = sqlparse.split(content)
        print(f"📄 Выполнение {script}.sql (найдено операторов: {len(statements)})")

        for idx, stmt in enumerate(statements, 1):
            clean_stmt = stmt.strip()
            if not clean_stmt:
                continue

            if clean_stmt.endswith(";"):
                clean_stmt = clean_stmt[:-1].strip()

            if not clean_stmt:
                continue

            print(f"\n▶ Оператор {idx}: {clean_stmt[:60]}{'...' if len(clean_stmt) > 60 else ''}")

            try:
                self.cursor.execute(clean_stmt)

                if self.cursor.with_rows:
                    rows = self.cursor.fetchall()
                    while self.cursor.nextset():
                        self.cursor.fetchall()
                    
                    if rows:
                        for row in rows:
                            print(row)
                    else:
                        print("(пустой результат)")
                elif self.cursor.rowcount > 0:
                    print(f"Затронуто строк: {self.cursor.rowcount}")

            except MySQLError as e:
                print(f"❌ Ошибка выполнения оператора:\n{clean_stmt}\n{e}")
                raise

        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    db = Database()
    
    db.run("fav_food")

    db.run_cli("sakila-schema")
    db.run_cli("sakila-data", database="sakila")
    
    db.use_database("sakila")
    db.run("sakila")

    db.close()