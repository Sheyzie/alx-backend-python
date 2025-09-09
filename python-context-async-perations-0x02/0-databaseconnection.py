'''
Class Based Context Manager
'''
import sqlite3

class DatabaseConnection:
    def __init__(self):
        print('Initializing DB connection')
        self.conn = sqlite3.connect('users_data.db')
        self.create_table()
        self.populate_table()


    def __enter__(self):
        print('Connecting to DB...')
        self.conn = sqlite3.connect('users_data.db')
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Closing DB connection')
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

with DatabaseConnection() as conn:
    if conn:
        print('Connected to DB')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    for user in users:
        print(user)
    cursor.close()
