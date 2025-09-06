'''
nstruction:

Implement a generator stream_user_ages() that yields user ages one by one.

Use the generator in a different function to calculate the average age without loading the entire dataset into memory

Your script should print Average age of users: average age

You must use no more than two loops in your script

You are not allowed to use the SQL AVERAGE
'''

#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    connection = seed.connect_to_prodev()

    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for row in cursor:
        yield row[0]

    connection.close()

def calculate_mean_age():
    iteration = 0
    age_sum = 0
    for age in stream_user_ages():
        iteration += 1
        age_sum += age
    average_age = age_sum / iteration
    print(f'Average age of users: {average_age}') 

calculate_mean_age()

