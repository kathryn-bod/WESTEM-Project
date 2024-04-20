import mysql.connector
from datetime import datetime
import uuid  # Import the uuid module to generate unique IDs

def generate_document_id():
    return str(uuid.uuid4()) 

def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        password='pass123',
        user='root',
        database="westem"
    )


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
    try:
        con = connect_to_database()
        cursor = con.cursor()

        # SQL query to retrieve user's documents based on username
        query = "SELECT * FROM documents WHERE user_id = %s"
        print("Executing query:", query)  # Debugging output
        cursor.execute(query, (username,))
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
    except mysql.connector.Error as err:
        print("Error:", err)

from datetime import datetime

def upload_document(username, title, doc_type, filename, document_timestamp=None):
    try:
        con = connect_to_database()
        cursor = con.cursor()

        # Retrieve user_id based on username
        query = "SELECT user_id FROM users WHERE username = %s"
        print("Executing query:", query)  # Debugging output
        cursor.execute(query, (username,))
        user_id = cursor.fetchone()[0]

        # Generate a unique document ID
        document_id = generate_document_id()
        print("Generated document ID:", document_id)  # Debugging output

        # Use current timestamp if document timestamp is not provided
        if document_timestamp is None:
            document_timestamp = datetime.now()

        # SQL query to upload new document
        insert_query = "INSERT INTO documents (document_id, title, type, filename, update_time, user_id, document_timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)"
        print("Executing query:", insert_query)  # Debugging output
        document_data = (document_id, title, doc_type, filename, user_id, document_timestamp)
        print("Data to insert:", document_data)  # Debugging output
        cursor.execute(insert_query, document_data)
        con.commit()  # Commit the transaction

        print("Document uploaded successfully.")

        con.close()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    except Exception as ex:
        print("Error:", ex)


def profile_options(username):
    while True:
        title = "Profile Options"
        option1 = "[1] View Profile"
        option3 = "[2] See Documents"
        option4 = "[3] Upload New Documents"
        option5 = "[4] Back"
        box_width = 100

        print("\033c\033[3J")
        print("╔" + "═" * (box_width - 2) + "╗")
        print("║" + title.center(box_width - 2) + "║")
        print("╠" + "═" * (box_width - 2) + "╣")
        print("║" + option1.center(box_width - 2) + "║")
        print("║" + option3.center(box_width - 2) + "║")
        print("║" + option4.center(box_width - 2) + "║")
        print("║" + option5.center(box_width - 2) + "║")
        print("╚" + "═" * (box_width - 2) + "╝")
        print()

        choice = input("Enter your choice: ")

        if choice == '1':
            edit_profile(username)
        elif choice == '2':
            see_documents(username)
        elif choice == '3':
            title = input("Enter document title: ")
            doc_type = input("Enter document type: ")
            filename = input("Enter filename: ")
            upload_document(username, title, doc_type, filename)
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")



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

