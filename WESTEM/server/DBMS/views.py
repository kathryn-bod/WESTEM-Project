import mysql.connector
import sqlite3


con = mysql.connector.connect(
    host='localhost', 
    password = 'pass123', 
    user='root',
    database = "westem")

if con.is_connected():
    print("Yes")


cursor = con.cursor()


def create_views(cursor):
    view1 = """
    CREATE VIEW user_project_summary AS
    SELECT 
        users.username,
        users.first_name,
        users.last_name,
        users.email,
        users.phone_number,
        COUNT(projects.project_id) AS project_count
    FROM users
    LEFT JOIN projects ON users.username = projects.user_id
    GROUP BY users.username;
    """
    
    view2 = """
    CREATE VIEW employee_mentorship_summary AS
    SELECT 
        employee.employer_id,
        employee.first_name,
        employee.last_name,
        employee.email,
        employee.phone_number,
        COUNT(mentorship.employee_id) AS mentorship_count
    FROM employee
    LEFT JOIN mentorship ON employee.employer_id = mentorship.employee_id
    GROUP BY employee.employer_id;
    """

    view3 = """
    CREATE VIEW user_resource_usage AS
    SELECT 
        users.username,
        users.first_name,
        users.last_name,
        resources.name AS resource_name,
        resources.resource_id,
        COUNT(resource_application.resource_id) AS usage_count
    FROM users
    JOIN resource_application ON users.username = resource_application.user_id
    JOIN resources ON resource_application.resource_id = resources.resource_id
    GROUP BY users.username, resources.resource_id;
    """

    cursor.execute(view1)
    cursor.execute(view2)
    cursor.execute(view3)
    print("Views created successfully.")

# Usage within your script
create_views(cursor)
con.commit()
