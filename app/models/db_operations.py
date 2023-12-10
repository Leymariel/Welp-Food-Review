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

    def get_row(self, table, IDvar, IDval, mult = False):
        query = f"SELECT * FROM {table} WHERE {IDvar} = '{IDval}'"
        self.cursor.execute(query)
        if mult:

            found = self.cursor.fetchall()
        else:
            found = self.cursor.fetchone()
        return found

    def send_query(self, query, params = None):
        try:
            
            self.cursor.execute(query, params)
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Failed to update record to database rollback: {error}")
            # rollback if any exception occured
            self.connection.rollback()
        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")


    def get_all(self, table, columns="*"):
        query = f"SELECT {columns} FROM {table}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results


    def get_all_query(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def get_agg(self, query):
        self.cursor.execute(query)
        found = self.cursor.fetchone()
        return found
    
    def get_categories(self):
        query = "SELECT CategoryID, CategoryName FROM Categories"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def get_category_id(self, category_name):
        query = "SELECT CategoryID FROM Categories WHERE CategoryName = %s"
        self.cursor.execute(query, (category_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_category_by_id(self, category_id):
        query = "SELECT CategoryName FROM Categories WHERE CategoryID = %s;"
        result = self.fetch_query(query, (category_id,))
        
        if result:
            return result[0][1]  # Assuming the second column (index 1) is CategoryName
        else:
            return None  # Return None if no category is found


        
    def get_category_name(self, category_id):
        try:
            query = "SELECT CategoryName FROM Categories WHERE CategoryID = %s"
            print(query)
            self.cursor.execute(query, (category_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as error:
            print(f"Error in get_category_name: {error}")
            return None

    def get_custom_query(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

