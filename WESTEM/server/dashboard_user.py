import mysql.connector
import time
from datetime import datetime
from datetime import datetime


def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        password='pass123',
        user='root',
        database="westem"
    )


counter = 0

def generate_document_id():
    global counter
    # Get current timestamp
    timestamp = int(time.time() * 1000)  # Convert to milliseconds
    # Increment counter to ensure uniqueness
    counter += 1
    # Combine timestamp and counter to generate ID
    # Limit the ID range to fit within the maximum value of INT
    document_id = (timestamp % (2**31)) * 1000 + counter
    return document_id


def edit_profile(username):
    try:
        con = connect_to_database()
        cursor = con.cursor()

        # SQL query to retrieve current profile information
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        current_profile_data = cursor.fetchone()

        if current_profile_data:
            print("Current Profile Information:")
            print("1. First Name:", current_profile_data[5])
            print("2. Last Name:", current_profile_data[6])
            print("3. Email:", current_profile_data[7])
            print("4. Address:", current_profile_data[1])
            print("5. Career Status:", current_profile_data[2])
            print("6. Date of Birth:", current_profile_data[3])
            print("7. Phone Number:", current_profile_data[8])

            changes = {}
            while True:
                choice = input("Enter the number corresponding to the field you want to edit (or 's' to save, 'd' to discard): ")
                if choice.lower() == 's':
                    for field, value in changes.items():
                        update_query = f"UPDATE users SET {field} = %s WHERE username = %s"
                        cursor.execute(update_query, (value, username))
                    con.commit()
                    print("Profile updated successfully.")
                    break
                elif choice.lower() == 'd':
                    print("Changes discarded.")
                    break
                elif choice.isdigit():
                    field_num = int(choice)
                    new_value = input("Enter the new value: ")

                    # Updating the selected field
                    if field_num == 1:
                        changes['first_name'] = new_value
                    elif field_num == 2:
                        changes['last_name'] = new_value
                    elif field_num == 3:
                        changes['email'] = new_value
                    elif field_num == 4:
                        changes['address'] = new_value
                    elif field_num == 5:
                        changes['career_status'] = new_value
                    elif field_num == 6:
                        changes['dob'] = datetime.strptime(new_value, "%Y-%m-%d").date()
                    elif field_num == 7:
                        changes['phone_number'] = new_value
                    else:
                        print("Invalid choice.")
                else:
                    print("Invalid input.")
        else:
            print("Profile not found.")

        con.close()
    except mysql.connector.Error as err:
        print("Error:", err)


def see_documents(username):
 
        con = connect_to_database()
        cursor = con.cursor()

        # Retrieve user_id based on username
        query = "SELECT username FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user_id = cursor.fetchone()[0]

        # SQL query to retrieve user's documents based on user_id
        query = "SELECT * FROM documents WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        documents = cursor.fetchall()

        if documents:
            print("Documents:")
            for doc in documents:
                print("Document ID:", doc[0])
                print("Title:", doc[1])
                print("Type:", doc[2])
                print("Filename:", doc[3])
                print("Update Time:", doc[4])
                print()
        else:
            print("No documents found.")

        con.close()

def upload_document(username, title, doc_type, filename, update_time=None):

        con = connect_to_database()
        cursor = con.cursor()

        # Retrieve user_id based on username
        query = "SELECT username FROM users WHERE username = %s"
        #print("Executing query:", query)  # Debugging output
        cursor.execute(query, (username,))
        user_id = cursor.fetchone()[0]

        # Generate a unique document ID
        document_id = generate_document_id()
        #print("Generated document ID:", document_id)  # Debugging output

        # Use current timestamp if document timestamp is not provided
        if update_time is None:
            update_time = datetime.now()

        # SQL query to upload new document
        insert_query = "INSERT INTO documents (document_id, title, type, filename, update_time, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
        #print("Executing query:", insert_query)  # Debugging output
        document_data = (document_id, title, doc_type, filename, update_time, user_id)
        #print("Data to insert:", document_data)  # Debugging output
        cursor.execute(insert_query, document_data)
        con.commit()  # Commit the transaction

        print("Document uploaded successfully.")


        con.close()
  


def profile_options(username):
    while True:
        title = "Profile Options"
        option1 = "[1] View Profile"
        option2 = "[2] See Documents"
        option3 = "[3] Upload New Documents"
        option4 = "[4] Back"
        box_width = 100

        print("\033c\033[3J")
        print("╔" + "═" * (box_width - 2) + "╗")
        print("║" + title.center(box_width - 2) + "║")
        print("╠" + "═" * (box_width - 2) + "╣")
        print("║" + option1.center(box_width - 2) + "║")
        print("║" + option2.center(box_width - 2) + "║")
        print("║" + option3.center(box_width - 2) + "║")
        print("║" + option4.center(box_width - 2) + "║")
        print("╚" + "═" * (box_width - 2) + "╝")
        print()

        choice = input("Enter your choice: ")

        if choice == '1':
            edit_profile(username)
        elif choice == '2':
            see_documents(username)
            input("Press Enter to return to the menu...")
        elif choice == '3':
            title = input("Enter document title: ")
            doc_type = input("Enter document type: ")
            filename = input("Enter filename: ")
            upload_document(username, title, doc_type, filename)
            input("Press Enter to return to the menu...")
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")




    try:
        con = connect_to_database()
        cursor = con.cursor()

        # Retrieve user_id based on username
        query = "SELECT username FROM users WHERE username = %s"
        print("Executing query:", query)  # Debugging output
        cursor.execute(query, (username,))
        user_id = cursor.fetchone()[0]

        # Generate a unique document ID
        document_id = generate_document_id()
        print("Generated document ID:", document_id)  # Debugging output

        # Use current timestamp if document timestamp is not provided
        if update_time is None:
            update_time = datetime.now()

        # SQL query to upload new document
        insert_query = "INSERT INTO documents (document_id, title, type, filename, update_time, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
        print("Executing query:", insert_query)  # Debugging output
        document_data = (document_id, title, doc_type, filename, update_time, user_id)
        print("Data to insert:", document_data)  # Debugging output
        cursor.execute(insert_query, document_data)
        con.commit()  # Commit the transaction

        print("Document uploaded successfully.")

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        con.close()

def user_menu(username):
    while True:
        option = "[P] Profile"
        option2 = "[M] Mentorships"
        option3 = "[W] Workshops"
        option4 = "[R] Resume"
        option5 = "[L] Logout"
        box_width = 100

        print("╔" + "═" * (box_width - 2) + "╗")
        print("║" + option.center(box_width - 2) + "║")
        print("║" + option2.center(box_width - 2) + "║")
        print("║" + option3.center(box_width - 2) + "║")
        print("║" + option4.center(box_width - 2) + "║")
        print("║" + option5.center(box_width - 2) + "║")
        print("╚" + "═" * (box_width - 2) + "╝")
        print()
        user_choice = input("Enter your choice: ")
        if user_choice.lower() == "p":
            print("\033c\033[3J")
            profile_options(username)
        elif user_choice.lower() == "m":
            pass  # Placeholder for mentorship functionality
        elif user_choice.lower() == "w":
            pass  # Placeholder for workshops functionality
        elif user_choice.lower() == "r":
            pass  # Placeholder for resume functionality
        elif user_choice.lower() == "l":
            print("\033c\033[3J")
            return -1
        elif user_choice == '2':  # Add this condition to call see_documents
            print("\033c\033[3J")
            see_documents(username)  # Call see_documents function
        else:
            print("Invalid input.")
            return True

def user_dashboard(username):
    title = "WESTEM"
    title2 = "USER DASHBOARD"

    # Define box width
    box_width = 100

    # Print title box
    print("\033c\033[3J")
    print("╔" + "═" * (box_width - 2) + "╗")
    print("║" + title.center(box_width - 2) + "║")
    print("║" + title2.center(box_width - 2) + "║")
    print("╚" + "═" * (box_width - 2) + "╝")
    print()

    text = "[D] Open Dashboard"
    text2 = "[L] Logout"
    print("╔" + "═" * (box_width - 2) + "╗")
    print("║" + text.center(box_width - 2) + "║")
    print("║" + text2.center(box_width - 2) + "║")
    print("╚" + "═" * (box_width - 2) + "╝")

    con = connect_to_database()
    cursor = con.cursor()

    user_option = input("Enter your choice: ")
    if user_option.lower() == 'd':
        print("\033c\033[3J") 
        user_menu(username)
    elif user_option.lower() == 'l':
        pass
    else:
        user_option = input("")

