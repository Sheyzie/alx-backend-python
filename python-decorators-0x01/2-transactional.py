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

def transactional(func):
    # manage db connection
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.pop('conn')
        # Access the attribute (if it exists)
        conn = conn if conn else getattr(func, "_custom_data", None)

        try:
            func(*args, **kwargs)
            conn.commit()
        except Exception as e:
            func(*args, **kwargs)
            conn.rollback()
            conn.close()
        conn.close()
        
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')