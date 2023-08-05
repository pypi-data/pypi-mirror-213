from mysql.connector import connect, DatabaseError

__all__ = (
    "Database"
)

class Database():
    def __init__(self, connection_config: dict):
        self.config = connection_config
        self.sql = {}
        
        def Establish():
            try:
                cnx = connect(
                    host=self.config["HOST"],
                    database=self.config["DATABASE"],
                    user=self.config["USER"],
                    password=self.config["PASSWORD"]
                )
                
                self.sql = {
                    "cursor": cnx.cursor(),
                    "commit": cnx.commit,
                    "establish": cnx.is_connected()
                }

            except Exception as error:
                errorcode = error.errno if hasattr(error, 'errno') else error
                self.sql["error"], self.sql["code"], self.sql["establish"] = True, errorcode, False

        Establish()


    def Connection(self):
        cb = {}
        cb["establish"] = self.sql["establish"]

        if not cb["establish"]:
            cb["error"] = self.sql["error"]
            cb["code"] = self.sql["code"]
            
        return cb
    
    def Query(self, params: str, method: str = "One") -> dict:
        query = {}
        execute = False

        if "error" in self.sql:
            query["error"] = "Unable to perform query."
            query["code"] = self.sql["code"]
            return query

        def refactore(column_names, query_values):
            return {column_names[i]: query_values[i] for i in range(len(column_names))}

        if any(keyword in params.upper() for keyword in ("UPDATE", "INSERT", "DELETE")):
            execute = True
            
        try:
            self.sql["cursor"].execute(params)
        except Exception as error:
            query["error"] = "Unable to perform query."
            query["code"] = error.errno
            return query

        if execute:
            self.sql["commit"]()
            query["executed"] = True
            return query

        if method != "One":
            query_response = self.sql["cursor"].fetchall()

            if query_response == None or len(query_response) <= 0:
                query["result"] = []
            else:
                query["result"] = [refactore(self.sql["cursor"].column_names, row) for row in query_response]
        
        else:
            query_response = self.sql["cursor"].fetchone()

            if query_response == None or len(query_response) <= 0:
                query["result"] = []
            else:  
                query["result"] = refactore(self.sql["cursor"].column_names, query_response)
        
        return query
    
    def Backup(self):
        backup = {}

        if "error" in self.sql or not self.sql["establish"]:
            backup["error"] = "Unable to perform backup."
            backup["code"] = self.sql["code"]
            return backup

        try:
            self.sql["cursor"].execute('SHOW TABLES')
            tables = self.sql["cursor"].fetchall()

            archive = open("backup.sql", 'w')

            for table in tables:
                table = table[0]
                self.sql["cursor"].execute(f'SELECT * FROM {table}')
                lines = self.sql["cursor"].fetchall()
                archive.write(f'-- PIITSZK BACKUP [TABLE]: {table}\n')
                archive.write(f'DROP TABLE IF EXISTS {table};\n')
                create_table = self.sql["cursor"].execute(f'SHOW CREATE TABLE {table}')
                create_table = self.sql["cursor"].fetchone()[1]
                archive.write(create_table + ';\n')
                for line in lines:
                    values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in line])
                    archive.write(f'INSERT INTO {table} VALUES ({values});\n')

            archive.close()
            backup["sucess"] = True
        except Exception as error:
            backup["error"] = f"Erro ao fazer o backup do banco de dados: {error}"
        
        return backup

