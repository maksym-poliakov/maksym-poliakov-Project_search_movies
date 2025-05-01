

import mysql.connector

from time import sleep
from config_sql_requests import add_limit_offset
from datetime import datetime


# class for working with a database
class DataBase :
    def __init__(self,param_connect,max_attempts,delay,seize_request,query_type,limit ):
        self.param_connect = param_connect
        self.max_attempts = max_attempts
        self.delay = delay
        # Size of the output result displayed on the screen
        self.seize_request = seize_request
        # Type of output results
        self.query_type = query_type
        # Number of output results
        self.limit = limit


    def get_seize_request(self) :
        return self.seize_request


    def db_connect(self) :
        conn = None
        attempt = 1
        while attempt <= self.max_attempts :
            try:
                conn = mysql.connector.connect(**self.param_connect)
                return conn
            except mysql.connector.Error :
                print(f'Error connecting to {self.param_connect.get('database')} database ')
                if attempt == self.max_attempts:
                    print("Max reconnection attempts reached. Failed to connect.")
                    raise ConnectionError  # None
                print(f"Reconnecting in {self.delay} seconds...")
                sleep(self.delay)
                attempt += 1
                print('Reconnecting')

        return  conn # None

    def create_table(self):
        """
        Creates a table for storing search queries.
        """
        conn = None
        cursor = None
        try:
            conn = self.db_connect()
            cursor = conn.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS search_queries (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        query_type VARCHAR(100),
                        query_text TEXT,
                        query_count INT DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE KEY uq_query_type_text (query_type, query_text(255))
                    )
                """)
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error creating table search_queries: {err}")
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()


    def save_search_query(self, query_type, query_text):
        """
        Inserts or updates a search query in the search_log table.
        """
        conn = None
        cursor = None
        try:
            conn = self.db_connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO search_queries (query_type, query_text, query_count, created_at)
                VALUES (%s, %s, 1, %s)
                ON DUPLICATE KEY UPDATE query_count = query_count + 1
            """, (query_type, query_text, datetime.now()))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error saving query: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_result_query(self,*request,type_request,offset):
        """
        Method for retrieving query results from the database.
        :param request: Query for selecting data from the database
        :param type_request: Type of result retrieval: 'all' - full query result, 'part' - partial query result
        :param offset: Number of results to output
        :return: Query result from the database
        """

        conn = None
        cursor = None
        try:
            conn = self.db_connect()

            if conn is None :
                print("Failed to connect to the database.")
                return None
            data = None

            # Cursor will return a dictionary
            cursor = conn.cursor(dictionary=True)
            query = request[0]
            params = request[1] if len(request) > 1 else ()

            # Modify the query for type_request='part'
            if type_request == 'part':
                query = add_limit_offset(query, offset,self.seize_request)

                if not query:
                    print("Ошибка: Не удалось модифицировать запрос")
                    return None
            # Execute the query
            if isinstance(params, tuple):
                cursor.execute(query, params)
            else:
                cursor.execute(query, (params,))
            if type_request == 'all' :
                data = cursor.fetchall()
                return data
            elif type_request == 'part' :
                data = cursor.fetchmany(self.seize_request)

            return data

        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")

            return None
        except TypeError as err:
            print(f"Parameter error: {err}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()