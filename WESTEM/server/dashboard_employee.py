import mysql.connector
import random

def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        password='pass123',
        user='root',
        database="westem"
    )

def generate_unique_resource_id(cursor):
    while True:
        resource_id = random.randint(100000, 999999)
        cursor.execute("SELECT COUNT(*) FROM resources WHERE resource_id = %s", (resource_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            # Unique resource_id found
            return resource_id


def show_workshops():
    con = connect_to_database()
    cursor = con.cursor()
    try:
        cursor.execute("SELECT workshop_name, duration, about FROM workshops")
        workshops = cursor.fetchall()
        if workshops:
            print("List of Workshops:")
            for workshop in workshops:
                workshop_name, duration, about = workshop
                print(f"Workshop Name: {workshop_name}")
                print(f"Duration: {duration} hours")
                print(f"About: {about}")
                print("-" * 50)
        else:
            print("There are no workshops currently being offered.")
    finally:
        cursor.close()
        con.close()

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


def workforWestem(user_in, employee_id):
    con = connect_to_database()
    cursor = con.cursor()
    try:
        while True: 
            box_width = 100
            overallTxt = "Resource Application Page"
            cancelTxt = "Enter C at any point to cancel this process."
            print("╔" + "═" * (box_width - 2) + "╗")
            print("║" + overallTxt.center(box_width - 2) + "║")
            print("║" + cancelTxt.center(box_width - 2) + "║")
            print("║" + " " * (box_width - 2) + "║")
            if user_in.lower() == 'a':
                mentorTxt = "Mentorship Application"
                print("║" + mentorTxt.center(box_width - 2) + "║")
                print("╚" + "═" * (box_width - 2) + "╝")
                print()
                what_in = type_for_proj()
                if what_in.lower() == 'c':
                    print("\033c\033[3J")
                    return -1
                else: 
                    # Check if the chosen project focus exists in the projects table
                    cursor.execute("SELECT * FROM projects WHERE type = %s", (what_in,))
                    project = cursor.fetchone()
                    if project:
                        # Project focus exists, proceed with mentorship application
                        name = "mentorship"
                        resource_id = generate_unique_resource_id(cursor)
                        cursor.execute("INSERT INTO resources (resource_id, name, employee_id) VALUES (%s, %s, %s)", (resource_id, name, employee_id))
                        con.commit()
                        print("Inserting into mentorship table:")
                        insert_mentorship_query = "INSERT INTO mentorship (user_id, project_id, employee_id) VALUES (%s, %s, %s)"
                        print("Insert Mentorship Query:", insert_mentorship_query)
                        print("Values:", (project[4], project[0], employee_id))
                        cursor.execute(insert_mentorship_query, (project[4], project[0], employee_id))
                        con.commit()
                        print("\033c\033[3J")
                        print("Mentorship application successful!")
                    else:
                        print("There are currently no projects that match that focus.\nWould you like to choose a different focus? (Y/N)\n")
                        choose = input()
                        if choose.lower() == 'n':
                            print("\033c\033[3J")
                            print("We apologize for the inconvenience, be sure to keep checking for projects of that variety if you are still interested in mentorship!")
                            return -1
                        elif choose.lower() == 'y':
                            print("\033c\033[3J")
                            return True 
                        else:
                            print("\033c\033[3J")
                            print("Invalid input. Returning you to the application page.")
                            workforWestem(user_in, employee_id)
                            
            elif user_in.lower() == 's':
                workshopTxt = "Workshop Signup"
                print("║" + workshopTxt.center(box_width - 2) + "║")
                print("╚" + "═" * (box_width - 2) + "╝")
                print()
                when_in = input("Duration of workshop:")
                if when_in.lower() == 'c' :
                    print("\033c\033[3J")
                    return -1
                else:
                    name_in = input("Workshop title:")
                    if name_in.lower() == 'c' :
                        print("\033c\033[3J")
                        return -1
                    else:
                        what_in = input("Workshop description: ")
                        if what_in.lower() == 'c' :
                            print("\033c\033[3J")
                            return -1
                        else:
                            name = "workshop"
                            resource_id = generate_unique_resource_id(cursor)
                            cursor.execute("INSERT INTO resources (resource_id, name, employee_id) VALUES (%s, %s, %s)", (resource_id, name, employee_id))
                            con.commit()
                            print("Inserting into workshops table:")
                            insert_workshop_query = "INSERT INTO workshops (resource_id, about, duration, workshop_name) VALUES (%s, %s, %s, %s)"
                            print("Insert Workshop Query:", insert_workshop_query)
                            print("Values:", (resource_id, what_in, when_in, name_in))
                            cursor.execute(insert_workshop_query, (resource_id, what_in, when_in, name_in))
                            con.commit()
                            print("Insertion into workshops table successful.")
                            print("\033c\033[3J")
                            print("Thank you for helping us by teaching this workshop!\nIt has been scheduled.")
                            break
            elif user_in.lower() == 'h':
                resumeTxt = "Resume Reviewing"
                print("║" + resumeTxt.center(box_width - 2) + "║")
                print("╚" + "═" * (box_width - 2) + "╝")
                print()
                check = input("Are you sure you want to review resumes for free? (Y/N)\n")
                if check.lower() == 'n' or check.lower() =='c':
                    print("\033c\033[3J")
                    print("If you ever change your mind, we would love to have your assistance!")
                    return -1
                elif check.lower() == 'y':
                    cursor.execute("SELECT first_name, last_name FROM employee WHERE employer_id = %s", (employee_id,))
                    rows = cursor.fetchall()
                    for row in rows: 
                        first = row[0]
                        last = row[1]
                    reviewer = first+" "+last
                    name = "resume review"
                    resource_id = generate_unique_resource_id(cursor)
                    cursor.execute("INSERT INTO resources (resource_id, name, employee_id) VALUES (%s, %s, %s)", (resource_id, name, employee_id))                    
                    con.commit()
                    print("Inserting into resume_review table:")
                    insert_review_query = "INSERT INTO resume_review (resource_id, reviewer) VALUES (%s, %s)"
                    print("Insert Review Query:", insert_review_query)
                    print("Values:", (resource_id, reviewer))
                    cursor.execute(insert_review_query, (resource_id, reviewer))
                    con.commit()
                    print("Insertion into resume_review table successful.")
                    print("\033c\033[3J")
                    print("Thank you for your assistance!\nYou will be notified when you are assigned a resume to review.")
                    break
    finally:
        cursor.close()
        con.close()

def employee_options(choice, employee_id):
    while True: 
        if choice.lower() == 'm':
            box_width = 100
            applytxt = "[A] Apply to be a Mentor"
            whattxt = "[W] What is the mentorship program at WESTEM?"
            project = "[I] Information about current mentorship projects"
            returntxt = "[B] Back to employee resources"
            print("╔" + "═" * (box_width - 2) + "╗")
            print("║" + whattxt.center(box_width - 2) + "║")
            print("║" + applytxt.center(box_width - 2) + "║")
            print("║" + project.center(box_width - 2) + "║")
            print("║" + returntxt.center(box_width - 2) + "║")
            print("╚" + "═" * (box_width - 2) + "╝")
            print()
            user_in = input("What would you like to do now?\nEnter your choice:")
            if user_in.lower() == "a":
                print("\033c\033[3J")
                workforWestem(user_in, employee_id)
            elif user_in.lower() == "i":
                pass
            elif user_in.lower() == "b":
                print("\033c\033[3J")
                return -1
            else: 
                print("\033c\033[3J")
                print("Invalid input. Re-enter your choice: ") 
                employee_options(choice, employee_id) 
        elif choice.lower() == 'w':
            box_width = 100
            signuptxt = "[S] Sign-up to teach a workshop"
            currentworkshops = "[L] List of upcoming workshops"
            returntxt = "[B] Back to employee resources"
            print("╔" + "═" * (box_width - 2) + "╗")
            print("║" + signuptxt.center(box_width - 2) + "║")
            print("║" + currentworkshops.center(box_width - 2) + "║")
            print("║" + returntxt.center(box_width - 2) + "║")
            print("╚" + "═" * (box_width - 2) + "╝")
            print()
            user_in = input("What would you like to do now?\nEnter your choice:")
            if user_in.lower() == "s":
                print("\033c\033[3J")
                workforWestem(user_in, employee_id)
            elif user_in.lower() == "l":
                print("\033c\033[3J")
                show_workshops()
                input("Press Enter to return to the menu...")
            elif user_in.lower() == "b":
                print("\033c\033[3J")
                return -1
            else: 
                print("\033c\033[3J")
                print("Invalid input. Re-enter your choice: ") 
                employee_options(choice, employee_id) 
        elif choice.lower() == 'r':
            box_width = 100
            resumehelp = "[H] Help review resumes!"
            returntxt = "[B] Back to employee resources"

            print("╔" + "═" * (box_width - 2) + "╗")
            print("║" + resumehelp.center(box_width - 2) + "║")
            print("║" + returntxt.center(box_width - 2) + "║")
            print("╚" + "═" * (box_width - 2) + "╝")
            print()

            user_in = input("What would you like to do now?\nEnter your choice:")
            if user_in.lower() == "h":
               print("\033c\033[3J")
               workforWestem(user_in, employee_id)
            elif user_in.lower() == "b":
                print("\033c\033[3J")
                return -1
            else: 
                print("\033c\033[3J")
                print("Invalid input. Re-enter your choice: ") 
                employee_options(choice, employee_id)
        else: 
            print("\033c\033[3J")
            print("Invalid input. Re-enter your choice: ") 
            employee_options(choice, employee_id)
 
def resource_menu(employee_id):
    while True:
        option = "[M] Mentor"
        option2 = "[W] Workshops"
        option3 = "[R] Resume Assistance"
        option4 = "[E] Exit this menu"
        box_width = 100

        print("╔" + "═" * (box_width - 2) + "╗")
        print("║" + option.center(box_width - 2) + "║")
        print("║" + option2.center(box_width - 2) + "║")
        print("║" + option3.center(box_width - 2) + "║")
        print("║" + option4.center(box_width - 2) + "║")
        print("╚" + "═" * (box_width - 2) + "╝")
        print()
        user_choice = input("Enter your choice: ")
        if user_choice.lower() in ("m", "w", "r"):
            print("\033c\033[3J")
            employee_options(user_choice, employee_id)
        elif user_choice.lower() == "e":
            print("\033c\033[3J")
            return -1
        else:
            print("Invalid input.")
            return True
        
def dashboard_employee(employee_id):
    title = "WESTEM"
    title2 = "EMPLOYEE DASHBOARD"

    # Define box width
    box_width = 100

    # Print title box
    print("\033c\033[3J")
    print("╔" + "═" * (box_width - 2) + "╗")
    print("║" + title.center(box_width - 2) + "║")
    print("║" + title2.center(box_width - 2) + "║")
    print("╚" + "═" * (box_width - 2) + "╝")
    print()

    text = "[R] Resources"
    text2 = "[B] Back to Main Menu"
    print("╔" + "═" * (box_width - 2) + "╗")
    print("║" + text.center(box_width - 2) + "║")
    print("║" + text2.center(box_width - 2) + "║")
    print("╚" + "═" * (box_width - 2) + "╝")

    user_option = input("Enter your choice: ")
    if user_option.lower() == 'r':
        print("\033c\033[3J") 
        resource_menu(employee_id)
    elif user_option.lower() == 'b':
        print("\033c\033[3J")
        return -1
    else: 
        user_option = input("Invalid input. Re-enter your choice: ")
        return True
