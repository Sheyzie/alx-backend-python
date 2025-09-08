import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    # manage db connection
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn')
        if not conn:
            conn = sqlite3.connect('users.db')
            # Attach custom attribute
            # wrapper._custom_data = conn
            kwargs['conn'] = conn
            func(*args, **kwargs)
        else:
            func(*args, **kwargs)
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query_cache[args] = func(*args, **kwargs)
        return query_cache
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")