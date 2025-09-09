'''
Context Manager for managing both connection and the query execution
'''
import sqlite3

class ExecuteQuery:
    def __init__(self, query=None, param=None):
        print('Initializing DB connection')
        self.conn = sqlite3.connect('users_data.db')
        self.create_table()
        self.populate_table()
        self.query = query
        self.param = param


    def __enter__(self):
        print('Connecting to DB...')
        self.conn = sqlite3.connect('users_data.db')
        self.cursor = self.conn.cursor()
        print(self.query)
        self.cursor.execute(self.query, (self.param,))
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Closing DB connection')
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER
                );
        ''')
        self.conn.commit()

    def populate_table(self):
        cursor = self.conn.cursor()

        cursor.execute('SELECT * FROM users;')

        users = cursor.fetchall()

        if len(users) == 0:
            cursor.execute('''
                    INSERT INTO users (name, email, age)VALUES (?, ?, ?);
            ''', ('John', 'john@mail.com', 35))
            cursor.execute('''
                    INSERT INTO users (name, email, age)VALUES (?, ?, ?);
            ''', ('James', 'james@mail.com', 35))
            cursor.execute('''
                    INSERT INTO users (name, email, age)VALUES (?, ?, ?);
            ''', ('Jimmy', 'jimmy@mail.com', 35))

            self.conn.commit()

query = "SELECT * FROM users WHERE age > ?;"
param = 25

with ExecuteQuery(query, param) as users:
    if users:
        for user in users:
            print(user)

