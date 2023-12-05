import mysql.connector

class db_operations:
    def __init__(self, dbName='sql3664132', user='sql3664132', password='MpTl3GKGRq', host='sql3.freemysqlhosting.net'):
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
        for row in rows:
            print(row)
        print("\n")

    def exists(self, table, IDvar, IDval):
        query = f"SELECT COUNT(*) FROM {table} WHERE {IDvar} = '{IDval}'"
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        return count

    def get_variable(self, table, IDvar, IDval, var):
        query = f"SELECT {var} FROM {table} WHERE {IDvar} = '{IDval}'"
        self.cursor.execute(query)
        found = self.cursor.fetchone()[0]
        return found

    def get_row(self, table, IDvar, IDval):
        query = f"SELECT * FROM {table} WHERE {IDvar} = '{IDval}'"
        self.cursor.execute(query)
        found = self.cursor.fetchone()
        return found

    def send_query(self, query):
        self.cursor.execute(query)
        self.handle_unread_result()  # Consume any remaining results
        self.connection.commit()
        return self.cursor.lastrowid


    def get_all(self, table):
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def handle_unread_result(self):
        while self.cursor.nextset():
            pass

    def get_all_query(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results