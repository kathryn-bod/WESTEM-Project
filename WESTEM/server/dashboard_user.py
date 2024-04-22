import mysql.connector
import time
from datetime import datetime
import random
from sqlalchemy import desc


def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        password='pass123',
        user='root',
        database="westem"
    )

counter=0

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





def project_id(cursor):
    while True:
        project_id = random.randint(10000000, 99999999) 
        cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
        if not cursor.fetchone():  
            return project_id
def type_for_proj():
        print("Select what type of project you would like to work on from the following list:")
        print("[D] Data Science")
        print("[W] Web Development")
        print("[B] Backend")
        print("[F] Frontend")
        print("[FS] Full Stack")
        type=input("Type: ")
        if type in ["D", "d"]:
            project_type= "Data Science"
        elif type in ["W", "w"]:
            project_type= "Web Development"
        elif type in ["B", "b"]:
            project_type= "Backend"
        elif type in ["F", "f"]:
            project_type="Frontend"
        elif type in ["FS", "fS", "Fs", "fs"]:
            project_type= "Full Stack"
        else:
           print("Invalid Project Type. You Must Select From the List Above.")
        return project_type

def project_interest(username):
        user_id=username
        emp_id= 1
        title = "Project Interest Form"
        desc="Please enter the following details to register your proposed project"
        box_width = 100
        print("╔" + "═" * (box_width - 2) + "╗")
        print("║" + title.center(box_width - 2) + "║")
        print("╠" + "═" * (box_width - 2) + "╣")
        print("║" + desc.center(box_width - 2) + "║")
        print("╚" + "═" * (box_width - 2) + "╝")
        print()
        
      
        con = connect_to_database()
        cursor = con.cursor()
        budget=float(input("Budget: "))
        proj_type= type_for_proj()
        proj_name=input("Project Title: ")
        pid = project_id(cursor)
        print("Generated project ID:", pid) 

        cursor.execute("INSERT INTO projects (project_id, budget, type, name, user_id) VALUES (%s, %s, %s, %s, %s)",
                           (pid, budget, proj_type, proj_name, user_id))
        #cursor.execute("SELECT employee_id FROM 
        #cursor.execute("SELECT project_id FROM projects WHERE user_id= %s", (username,))
        #cursor.execute("SELECT project_id FROM projects WHERE user_id= %s", (username,))
        #mentorship_pid= cursor.fetchone()[0]
        #cursor.execute("INSERT INTO mentorship (user_id, project_id) VALUES (%s, %s)", (username, mentorship_pid))

        con.commit()
        print("Your project was registered sucessfully and is awaiting review.")


        #assign_mentor_to_project(pid)

        con.close()
        return


def project_status(username):
    try:
        con = connect_to_database()
        cursor = con.cursor()

        # Query the projects table to fetch the project ID based on the username
        query_fetch_project_id = "SELECT project_id FROM projects WHERE user_id = %s"
        cursor.execute(query_fetch_project_id, (username,))
        project_id = cursor.fetchone()

        #assign_mentor(project_id, username)

        if project_id:
            project_id = project_id[0]

            # Query the mentorship table to check if a mentor is assigned to the project
            query_check_mentorship = "SELECT r.name FROM mentorship m JOIN resources r ON m.employee_id = r.employee_id WHERE m.project_id = %s"
            cursor.execute(query_check_mentorship, (project_id,))
            mentor_data = cursor.fetchone()

            if mentor_data:
                mentor_name = mentor_data[0]
                print("Project Status:")
                print("Mentor assigned to the project:", mentor_name)
            else:
                print("No mentor assigned to the project.")
        else:
            print("No project found for the provided username.")

        con.close()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    except Exception as ex:
        print("Error:", ex)


def view_proj(username):
     title = "Current Projects"
     box_width = 100
     print("╔" + "═" * (box_width - 2) + "╗")
     print("║" + title.center(box_width - 2) + "║")
     #print("╠" + "═" * (box_width - 2) + "╣")
     print("╚" + "═" * (box_width - 2) + "╝")
     try:
        con = connect_to_database()
        cursor = con.cursor()

        # SQL query to retrieve current profile information
        query = "SELECT * FROM projects WHERE user_id = %s"
        cursor.execute(query, (username,))
        curr_projects = cursor.fetchone()

        if curr_projects:
            for projects in curr_projects:
                print("Current Profile Information:")
                print("1. Project Title:", curr_projects[3])
                print("2. Type:", curr_projects[2])
                print("2. Budget:", curr_projects[1])
                print("\n\n")
        con.close()

     except mysql.connector.Error as err:
        print("MySQL Error:", err)
     except Exception as ex:
        print("Error:", ex)

        

def mentorship_signup(username):
    while True:
        title = "Mentorship"
        desc= """
        Welcome to WESTEM's Mentorship Program! In this Program you have the chance to work with our 
        brilliant Mentors who will guide you through your own personal project. This is a great chance 
        to recieve advice and supervision to help you enter and succeed in the technological industry. 
        Below you may fill out the Project Interest Form, and you will be paired with a mentor based off 
        of your input."""
        option1 = "[1] Project Interest Form"
        option2 = "[2] View Projects"
        option3 = "[3] Check Status for Project"
        option4 = "[3] Back"
        box_width = 100

        print("\033c\033[3J")
        print("╔" + "═" * (box_width - 2) + "╗")
        print("║" + title.center(box_width - 2) + "║")
        print("╠" + "═" * (box_width - 2) + "╣")
        lines = desc.strip().split("\n")
        for line in lines:
            print("│" + line.strip().center(box_width - 2) + "│")
        print("╠" + "═" * (box_width - 2) + "╣")
        print("║" + option1.center(box_width - 2) + "║")
        print("║" + option2.center(box_width - 2) + "║")
        print("║" + option3.center(box_width - 2) + "║")
        print("║" + option4.center(box_width - 2) + "║")
        print("╚" + "═" * (box_width - 2) + "╝")
        print()

        choice=input("Enter your choice: ")
        if choice=='1':
            project_interest(username)
            input("Press Enter to return to the menu...")
        elif choice=='2':
            view_proj(username)
            input("Press Enter to return to the menu...")
        elif choice == '3':
            #assign_mentor(project_id, username)
            project_status(username)
            input("Press Enter to return to the menu...")
        elif choice =='4':
            return
        else:
            print("Invalid choice. Please try again.")

def view_workshops(username):
    try:
        con=connect_to_database()
        cursor=con.cursor()

        cursor.execute("SELECT * FROM WORKSHOPS")
        wks=cursor.fetchall()

        if not wks:
            print("There are no scheduled workshops at this time.\n\n")
        else:
            title="Available Workshops"
            print("\033c\033[3J")
            box_width=100
            print("╔" + "═" * (box_width - 2) + "╗")
            print("║" + title.center(box_width - 2) + "║")
            print("╠" + "═" * (box_width - 2) + "╣")
            print()
            for w in wks:
                print("Resource ID:", wks[0])
                print("Duration:", wks[1])
        con.close()
    except mysql.connector.Error as err:
        print("Error:", err)


def resource_id(cursor):
    while True:
        resource_id = random.randint(10000000, 99999999) 
        cursor.execute("SELECT * FROM resume_review WHERE resource_id = %s", (resource_id,))
        if not cursor.fetchone():  
            return resource_id
        
def apply_resume_review(usern, filen):
    print("Resume Review")
    con = connect_to_database()
    cursor = con.cursor()

    cursor.execute("SELECT resource_id FROM resources WHERE name = 'resume review'")
    resume_resource = cursor.fetchone()
    cursor.fetchall()
    con.close()

    if resume_resource:
        resource_id = resume_resource[0]
        print("Found resume resource with ID:", resource_id)
        print("User ID:", usern)
        print("File name:", filen)

        con = connect_to_database()
        cursor = con.cursor()

        cursor.execute("SELECT document_id FROM documents WHERE user_id = %s AND filename = %s ORDER BY update_time DESC LIMIT 1", (usern, filen))
        doc_id_result = cursor.fetchone()

        if doc_id_result:
            doc_id = doc_id_result[0]
            print("Found resume document with ID:", doc_id)
            # Insert into resource_application and resume_review tables
            # cursor.execute("INSERT INTO resource_application (user_id, resource_id, document_id) VALUES (%s, %s, %s)", (usern, resource_id, doc_id))
            # cursor.execute("INSERT INTO resume_review (resource_id) VALUES (%s)", (resource_id,))
            # print("You are now registered for resume review.")
            # con.commit()
        else:
            print("No resume document found.")
    else:
        print("No resume resource found.")

    # Make sure to fetch all results before closing the cursor
    cursor.fetchall()
    # con.close()




def resume_menu(username):
    filename = "resume"
    while True:
        title = "Resume Menu"
        option1 = "[1] Submit Resume"
        option2 = "[2] Apply for Resume Review"
        option3 = "[3] Back"
        box_width = 100

        print("\033c\033[3J")
        print("╔" + "═" * (box_width - 2) + "╗")
        print("║" + title.center(box_width - 2) + "║")
        print("╠" + "═" * (box_width - 2) + "╣")
        #print("╠" + "═" * (box_width - 2) + "╣")
        print("║" + option1.center(box_width - 2) + "║")
        print("║" + option2.center(box_width - 2) + "║")
        print("║" + option3.center(box_width - 2) + "║")
        print("╚" + "═" * (box_width - 2) + "╝")
        print()   
        user_choice = input("Enter your choice: ")
        if user_choice == "1":
            print("\033c\033[3J")
            title = input("Enter document title: ")
            doc_type = input("Enter document type: ")
            upload_document(username, title, doc_type, filename)
            input("Press Enter to return to the menu...")
        elif user_choice == "2":
            print("\033c\033[3J")
            apply_resume_review(username, filename)
            input("Press Enter to return to the menu...")
        elif user_choice == "3":
            return
        else: 
            print("Invalid choice. Please try again.")


def user_menu(username):
    while True:
        option = "[P] Profile"
        option2 = "[M] Mentorship"
        option3 = "[W] Workshops"
        option4 = "[R] Resume"
        option5 = "[L] Logout"
        option6= "[O] Other Resources"
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
            print("\033c\033[3J")
            mentorship_signup(username)
        elif user_choice.lower() == "w":
             print("\033c\033[3J")
             view_workshops(username)
        elif user_choice.lower() == "r":
             print("\033c\033[3J")
             resume_menu(username)
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
