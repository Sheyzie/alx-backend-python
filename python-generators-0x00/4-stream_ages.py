'''
nstruction:

Implement a generator stream_user_ages() that yields user ages one by one.

Use the generator in a different function to calculate the average age without loading the entire dataset into memory

Your script should print Average age of users: average age

You must use no more than two loops in your script

You are not allowed to use the SQL AVERAGE
'''

#!/usr/bin/python3
from seed import connect_to_prodev

def stream_user_ages():
    connection = connect_to_prodev()

    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for age in cursor:
        yield age[0]

    connection.close()

def calculate_average_age():
    count = 0
    total = 0
    for age in stream_user_ages():
        count += 1
        total += age
    if count == 0:
        return 0
    return total / count
    # print(f'Average age of users: {average_age}') 

print('Average age of users:', calculate_average_age())

