import mysql.connector

# Function to establish database connection
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='pass123',
        database='westem'
    )

# Function to create triggers
def create_triggers():
    try:
        # Establish database connection
        con = connect_to_database()
        cursor = con.cursor()

        # Trigger to Prevent Duplicate Usernames for Users
        cursor.execute("""
            CREATE TRIGGER check_duplicate_username_users
            BEFORE INSERT ON users
            FOR EACH ROW
            BEGIN
                DECLARE is_duplicate INT;

                SELECT COUNT(*) INTO is_duplicate FROM users WHERE username = NEW.username;

                IF is_duplicate > 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate username not allowed';
                END IF;
            END
        """)

        # Trigger to Prevent Duplicate Usernames for Employees
        cursor.execute("""
            CREATE TRIGGER check_duplicate_employee_username
            BEFORE INSERT ON employee
            FOR EACH ROW
            BEGIN
                DECLARE is_duplicate INT;

                SELECT COUNT(*) INTO is_duplicate FROM employee WHERE username = NEW.username;

                IF is_duplicate > 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate employee username not allowed';
                END IF;
            END
        """)

        # Trigger to Prevent Duplicate Employee IDs for Employees
        cursor.execute("""
            CREATE TRIGGER check_duplicate_employee_id
            BEFORE INSERT ON employee
            FOR EACH ROW
            BEGIN
                DECLARE is_duplicate INT;

                SELECT COUNT(*) INTO is_duplicate FROM employee WHERE employer_id = NEW.employer_id;

                IF is_duplicate > 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate employee ID not allowed';
                END IF;
            END
        """)

        print("Triggers created successfully.")

    except mysql.connector.Error as err:
        print("Error creating triggers:", err)

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals() and con.is_connected():
            con.close()

# Execute the function to create triggers
create_triggers()
