import sqlite3
import functools

#### decorator to lof SQL queries
def log_queries(func):
    '''
    Decorator to log the query
    '''
    def wrapper(*args, **kwargs):
        # create user table

        query = kwargs.get('query')
        print(query)

        func(*args, **kwargs)
    return wrapper

def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        )
    '''
    )

    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))
    conn.commit()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

create_table()
#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)