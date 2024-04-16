import mysql.connector
import datetime
import random
import string



from server.helper.id_generator import employee_id

# Function to establish database connection
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        password='pass123',
        user='root',
        database="westem"
    )

# Function to handle user registration
def register_user(cursor, con):
    print("\nPlease provide the following details to create an account:")
    username = input("Username: ")
    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print("Username already exists. Please choose a different one.")
        return
    address = input("Address: ")
    career_status = input("Career Status: ")

    # Handle Date of Birth input with error handling
    while True:
        dob = input("Date of Birth (YYYY-MM-DD): ")
        try:
            # Attempt to convert the input string to a date
            dob_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
            break  # Break out of the loop if conversion is successful
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone_number = input("Phone Number: ")

    # Insert user details into the database
    insert_query = "INSERT INTO users (username, address, career_status, dob, password, first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (username, address, career_status, dob, password, first_name, last_name, email, phone_number))
    con.commit()
    print("Account created successfully!")

# Function to handle user login
def login_user(cursor):
    print("\nPlease enter your credentials to log in:")
    username = input("Username: ")
    password = input("Password: ")
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"Welcome back, {user[5]}!")
    else:
        print("Invalid username or password. Please try again.")


def register_employee(cursor, con):
    print("\nPlease provide the following details to create an employee account:")
    password = input("Password: ")
    email = input("Email: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    
    # Handle Date of Birth input with error handling
    while True:
        dob = input("Date of Birth (YYYY-MM-DD): ")
        try:
            # Attempt to convert the input string to a date
            dob_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
            break  # Break out of the loop if conversion is successful
        except ValueError:
            print("Invalid date format. Please enter the date of birth in YYYY-MM-DD format.")

    address = input("Address: ")
    phone_number = input("Phone Number: ")
    experience = input("Experience: ")

    # Generate a unique employee ID
    emp_id = employee_id(cursor)

    # Insert employee details into the database
    insert_query = "INSERT INTO employee (employer_id, password, email, first_name, last_name, dob, address, phone_number, experience) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (emp_id, password, email, first_name, last_name, dob, address, phone_number, experience))
    con.commit()
    print("Employee account created successfully! Your Employee ID is:", emp_id)

# Function to handle employee login
def login_employee(cursor):
    print("\nPlease enter your credentials to log in:")
    employee_id = input("Employee ID: ")
    password = input("Password: ")
    cursor.execute("SELECT * FROM employee WHERE employer_id = %s AND password = %s", (employee_id, password))
    employee = cursor.fetchone()
    if employee:
        print(f"Welcome back, {employee[3]}!")
    else:
        print("Invalid Employee ID or password. Please try again.")

# Function to handle employee sign-in
def employee_sign_in(cursor, con):
    while True:
        print("\nEmployee Sign In\n")
        print("1. Sign In")
        print("2. Create an Account")
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == '1':
            login_employee(cursor)
        elif choice == '2':
            register_employee(cursor, con)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

# Main function
def log_in_main():
    con = connect_to_database()
    cursor = con.cursor()

    while True:
        print("\nWelcome to the WESTEM!\n")
        print("1. Create an Account")
        print("2. Log In")
        print("3. Employee Sign In")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_user(cursor, con)
        elif choice == '2':
            login_user(cursor)
        elif choice == '3':
            employee_sign_in(cursor, con)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

    cursor.close()
    con.close()

if __name__ == "__main__":
    log_in_main()