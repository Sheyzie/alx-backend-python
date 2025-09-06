'''
Instructions:

Implement a generator function lazypaginate(pagesize) that implements the paginate_users(page_size, offset) that will only fetch the next page when needed at an offset of 0.

You must only use one loop
Include the paginate_users function in your code
You must use the yield generator
Prototype:
def lazy_paginate(page_size)
'''

#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()

    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of users using a single loop.
    
    Args:
        page_size (int): Number of users per page.
        
    Yields:
        A list of users in each page.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Example usage:
if __name__ == "__main__":
    for page in lazy_paginate(25):
        print(page)