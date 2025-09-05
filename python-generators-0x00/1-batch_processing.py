'''
Instructions:

Write a function stream_users_in_batches(batch_size) that fetches rows in batches

Write a function batch_processing() that processes each batch to filter users over the age of25`

You must use no more than 3 loops in your code. Your script must use the yield generator

Prototypes:

def stream_users_in_batches(batch_size)
def batch_processing(batch_size)
'''

seed = __import__('seed')


def stream_users_in_batches(batch_size):
    connection = seed.connect_to_prodev()

    if connection:
        cursor = connection.cursor(dictionary=True) # will return dictionary instead of tuple
        cursor.execute(f"SELECT * FROM user_data;")
        rows = cursor.fetchall()

        total_users = len(rows)
        for i in range(0, total_users, batch_size):
            yield rows[i:i + batch_size]

    
def batch_processing(batch_size):
    """Processes user batches, filtering users over the age of 25."""

    def process_filter(batch_size):
        for batch in stream_users_in_batches(batch_size):
            filtered_users = [user for user in batch if user['age'] > 25]
            yield filtered_users

    for batch in process_filter(batch_size):
        print(batch)



   
        