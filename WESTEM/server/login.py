from server.helper.id_generator import employee_id
import mysql.connector
import datetime
import re
import bcrypt


from server.dashboard_user import user_dashboard
from server.dashboard_employee import dashboard_employee


# Global variables to track user and employee login status
logged_in_user = None
logged_in_employee = None

# Function to establish database connection
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='pass123',
        database='westem'
    )


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[\@\#\$\%\&\*\!\?]', password):
        return False, "Password must contain at least one special character (@, #, $, %, &, *, !, ?)."
    return True, "Password is valid."

# Function to handle user registration
def register_user(cursor, con):
    global logged_in_user
    print("Please provide the following details to create an account:")
    username = input("Username: ")
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print("Username already exists. Please choose a different one.")
        return
    while True:
        password = input("Password (8 chars, upper, lower, digit, special): ")
        valid, message = validate_password(password)
        if valid:
            break
        else:
            print(message)
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone_number = input("Phone Number: ")
    address = input("Address: ")
    dob = input("Date of Birth (YYYY-MM-DD): ")

    # Hash password before saving to database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("INSERT INTO users (username, password, first_name, last_name, email, phone_number, address, dob) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, hashed_password, first_name, last_name, email, phone_number, address, dob))
    con.commit()
    print("User registered successfully!")
    logged_in_user = username


# Function to handle employee registration
def register_employee(cursor, con):
    global logged_in_employee
    print("Please provide the following details to create an employee account:")
    emp_id = employee_id(cursor)
    while True:
        username = input("Username: ")
        password = input("Password (8 chars, upper, lower, digit, special): ")
        valid, message = validate_password(password)
        if valid:
            break
        else:
            print(message)
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone_number = input("Phone Number: ")
    address = input("Address: ")
    dob = input("Date of Birth (YYYY-MM-DD): ")

    # Hash password before saving to database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("INSERT INTO employee (employer_id, username, password, first_name, last_name, email, phone_number, address, dob) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (emp_id, username, hashed_password, first_name, last_name, email, phone_number, address, dob))
    con.commit()
    print("Employee registered successfully! Your Employee ID is:", emp_id)
    logged_in_employee = emp_id

# Login functions for users and employees
def login_user(cursor):
    global logged_in_user
    username = input("Username: ")
    password = input("Password: ")
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        print(f"Welcome back, {username}!")
        logged_in_user = username
    else:
        print("Invalid credentials.")


def login_employee(cursor):
    #global logged_in_employee
    username = input("Username: ")
    password = input("Password: ")
    cursor.execute("SELECT employer_id, password FROM employee WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
        employee_id = result[0]
        print(f"Welcome back, Employee {employee_id}!")
        logged_in_employee = employee_id
        dashboard_employee(logged_in_employee)
    else:
        print("Invalid credentials.")


# Logout functions for users and employees
def logout_user():
    global logged_in_user
    print(f"Goodbye, {logged_in_user}!")
    logged_in_user = None

def logout_employee():
    global logged_in_employee
    print(f"Goodbye, Employee {logged_in_employee}!")
    logged_in_employee = None

# Information menu
def informational_menu():
    while True:
        print("\nInformation Menu")
        print("1. About Us")
        print("2. Policies")
        print("3. Stories About the Website")
        print("4. Back")
        choice = input("Enter your choice: ")
        if choice == '4':
            break
        elif choice == '1':
            print("About Us: We are dedicated to providing the best service.")
        elif choice == '2':
            print("Policies: Here are our user and privacy policies.")
        elif choice == '3':
            print("Stories: Read about our community's experiences.")
        else:
            print("Invalid choice. Please try again.")

"""
def indexing(cursor):
    try:
        cursor.execute("CREATE INDEX idx_emp_password ON employee(password)")
    except mysql.connector.Error as err:
        print("Error:", err)
    try:
         cursor.execute("CREATE INDEX idx_username ON users(username)")
    except mysql.connector.Error as err:
        print("Error:", err)
    try:
         cursor.execute("CREATE INDEX idx_emp_id on employee(employee_id)")
    except mysql.connector.Error as err:
        print("Error:", err)
""" 

# Main menu that handles different states based on login
def main_menu(cursor, con):
    #indexing(cursor)
    while True:
        print("\nMain Menu")
        if logged_in_user or logged_in_employee:
            print("1. Log Out")
            print("2. Sign Up/Sign In for Resources")
        else:
            print("1. User Log In")
            print("2. Employee Log In")
            print("3. Register User")
            print("4. Register Employee")
        print("5. Information")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1' and (logged_in_user or logged_in_employee):
            if logged_in_user:
                logout_user()
            else:
                logout_employee()
        elif choice == '1':
            login_user(cursor)
        elif choice == '2' and not (logged_in_user or logged_in_employee):
            login_employee(cursor)
        elif choice == '3' and not logged_in_employee:
            register_user(cursor, con)
        elif choice == '4' and not logged_in_employee:
            register_employee(cursor, con)
        elif choice == '2' and (logged_in_user or logged_in_employee):
            print("Resource sign-up/sign-in functionality to be implemented.")
            if logged_in_user:
                user_dashboard(logged_in_user)
            if logged_in_employee:
                dashboard_employee(logged_in_employee)
        elif choice == '5':
            informational_menu()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


def log_in_main():
    con = connect_to_database()
    cursor = con.cursor()
    main_menu(cursor, con)
    cursor.close()
    con.close()

if __name__ == "__main__":
    log_in_main()
