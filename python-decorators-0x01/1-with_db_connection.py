import sqlite3 
import functools


def with_db_connection(func):
    # manage db connection
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn')
        if not conn:
            conn = sqlite3.connect('users.db')
            func(conn, *args, **kwargs)
        else:
            func(*args, **kwargs)
        conn.close()
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)