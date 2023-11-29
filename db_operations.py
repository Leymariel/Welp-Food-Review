import mysql.connector

# class responsible for database operations
class db_operations():
    def __init__(self,dbName, user = 'sql3664132', password = 'MpTl3GKGRq', host = 'sql3.freemysqlhosting.net' ):
        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': dbName,
            'raise_on_warnings': True
            }
        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
            print("success")

        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def destructor(self):
        if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")
    
    def PrintDB(self):
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()

        for table_name in tables:
            print(f"Contents of table {table_name[0]}:")

            # Querying each table
            self.cursor.execute(f"SELECT * FROM {table_name[0]}")
            rows = self.cursor.fetchall()

            # Printing the contents of each table
            for row in rows:
                print(row)
            print("\n")
    
    def exists(self, table, IDvar, IDval):
        query = f'''
        SELECT COUNT(*)
        FROM {table}
        WHERE {IDvar} = '{IDval}'
        '''
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        return count
    
    