import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        password='pass123',
        user='root',
        database="westem"
    )

def workforWestem(user_in, employee_id, cursor, con):
    while True: 
        box_width = 100
        overallTxt = "Resource Application Page"
        cancelTxt = "Enter C at any point to cancel your application process."
        print("╔" + "═" * (box_width - 2) + "╗")
        print("║" + overallTxt.center(box_width - 2) + "║")
        print("║" + cancelTxt.center(box_width - 2) + "║")
        print("║" + " " * (box_width - 2) + "║")
        #print("╚" + "═" * (box_width - 2) + "╝")
        if user_in.lower() == 'a':
            mentorTxt = "Mentorship Application"
            #print("╔" + "═" * (box_width - 2) + "╗")
            print("║" + mentorTxt.center(box_width - 2) + "║")
            print("╚" + "═" * (box_width - 2) + "╝")
            print()
            why_in = input("Why do you want to be a mentor?")
            if why_in.lower() == 'c':
                print("\033c\033[3J")
                return -1
        elif user_in.lower() == 's':
            workshopTxt = "Workshop Signup"
            #print("╔" + "═" * (box_width - 2) + "╗")
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
                
                    
            #insert employee info and workshop info into workshop tableINSERT INTO mentorship_program (resource_id, resource_id, mentor)
        elif user_in.lower() == 'h':
            resumeTxt = "Resume Reviewing"
            #print("╔" + "═" * (box_width - 2) + "╗")
            print("║" + resumeTxt.center(box_width - 2) + "║")
            print("╚" + "═" * (box_width - 2) + "╝")
            print()
            check = input("Are you sure you want to review resumes for free? (Y/N)\n")
            if check.lower() == 'n' or check.lower() =='c':
                #insert employee info into resume_review table
                print("\033c\033[3J")
                print("If you ever change your mind, we would love to have your assistance!")
                return -1
            elif check.lower() == 'y':
                print("Thank you for your assistance!\nYou will be notified when you are assigned a resume to review.")
                cursor.execute("SELECT first_name, last_name FROM employee WHERE employer_id = %s", (employee_id,))
                con.commit()
                rows = cursor.fetchall()
                for row in rows: 
                    first = row[0]
                    last = row[1]
                reviewer = first+" "+last
                name = "resume review"
                cursor.execute("INSERT INTO resources (name, employee_id) VALUES (%s, %s)", (name, employee_id))
                con.commit()
                #cursor.execute("SELECT resource_id FROM resources WHERE employee_id = %s", (employee_id))
                #resource = cursor.fetchone()
                break




def employee_options(choice, employee_id, cursor, con):
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
                workforWestem(user_in, employee_id, cursor, con)
            elif user_in.lower() == "i":
                pass
            elif user_in.lower() == "b":
                pass
            else: 
                print("\033c\033[3J")
                print("Invalid input. Re-enter your choice: ") 
                employee_options(choice, employee_id,  cursor, con) 
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
                workforWestem(user_in, employee_id, cursor, con)
            elif user_in.lower() == "l":
                pass
            elif user_in.lower() == "b":
                print("\033c\033[3J")
                return -1
            else: 
                print("\033c\033[3J")
                print("Invalid input. Re-enter your choice: ") 
                employee_options(choice, employee_id, cursor, con) 
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
               workforWestem(user_in, employee_id, cursor, con)
            elif user_in.lower() == "b":
                print("\033c\033[3J")
                return -1
            else: 
                print("\033c\033[3J")
                print("Invalid input. Re-enter your choice: ") 
                employee_options(choice, employee_id, cursor, con)
        else: 
            print("\033c\033[3J")
            print("Invalid input. Re-enter your choice: ") 
            employee_options(choice, employee_id, cursor, con)
 
def resource_menu(employee_id, cursor, con):
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
            employee_options(user_choice, employee_id, cursor, con)
        elif user_choice.lower() == "e":
            print("\033c\033[3J")
            return -1
        else:
            print("Invalid input.")
            return True

def dashboard_employee(employee_id):
    con = connect_to_database()
    cursor = con.cursor()

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
    text2 = "[L] Logout"
    text3 = "[B] Back to Main Menu"
    print("╔" + "═" * (box_width - 2) + "╗")
    print("║" + text.center(box_width - 2) + "║")
    print("║" + text2.center(box_width - 2) + "║")
    print("╚" + "═" * (box_width - 2) + "╝")

    con = connect_to_database()
    cursor = con.cursor()
    user_option = input("Enter your choice: ")
    if user_option.lower() == 'r':
        print("\033c\033[3J") 
        resource_menu(employee_id, cursor, con)
    elif user_option.lower() == 'b':
        print("\033c\033[3J")
        return -1
    else: 
        user_option = input("Invalid input. Re-enter your choice: ")
        return True

