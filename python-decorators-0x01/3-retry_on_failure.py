import time
import sqlite3 
import functools

def with_db_connection(func):
    # manage db connection
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn')
        if not conn:
            conn = sqlite3.connect('users.db')
            # Attach custom attribute
            wrapper._custom_data = conn
            kwargs['conn'] = conn
            return func(conn, *args, **kwargs)
        else:
            func(*args, **kwargs)
            conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=1):
    def retry_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts_left = retries
            while attempts_left > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts_left -= 1
                    print(f"[Retry] Caught exception: {e}. Retries left: {attempts_left}")
                    if attempts_left == 0:
                        print("No retries left. Raising exception.")
                        raise
                    time.sleep(delay)
        return wrapper
    return retry_decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)