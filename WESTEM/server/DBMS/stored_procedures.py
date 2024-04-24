import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='pass123',
        database='westem'
    )

#create triggers
def create_triggers():
    try:
       
        con = connect_to_database()
        cursor = con.cursor()

        
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

        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals() and con.is_connected():
            con.close()


create_triggers()
