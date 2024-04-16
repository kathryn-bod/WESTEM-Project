import mysql.connector
import datetime
import random
import string

# Function to establish database connection
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        password='LgftugdSe34)$',
        user='root',
        database="westem"
    )


# Function to generate a unique employee ID
def employee_id(cursor):
    while True:
        employee_id = random.randint(10000000, 99999999)  # Generate a random 8-digit integer
        cursor.execute("SELECT * FROM employee WHERE employer_id = %s", (employee_id,))
        if not cursor.fetchone():  # Check if employee ID doesn't already exist
            return employee_id