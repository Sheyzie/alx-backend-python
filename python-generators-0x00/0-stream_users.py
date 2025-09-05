'''
Objective: create a generator that streams rows from an SQL database one by one.

Instructions:

In 0-stream_users.py write a function that uses a generator to fetch rows one by one from the user_data table. You must use the Yield python generator

Prototype: def stream_users()
Your function should have no more than 1 loop
'''

seed = __import__('seed')

def stream_users():
    connection = seed.connect_to_prodev()

    if connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM user_data;")
        rows = cursor.fetchall()
        # print(rows)
        num = 0
        while num < len(rows):
            yield rows[num]
            num += 1

