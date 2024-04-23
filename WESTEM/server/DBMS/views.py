import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        password='pass123',
        user='root',
        database="westem"
    )

def create_views():
    views = [
        """
        CREATE VIEW current_projects_view AS
        SELECT p.project_id, p.name AS project_title, p.type AS project_type, p.budget, m.employee_id
        FROM projects p
        INNER JOIN mentorship m ON p.project_id = m.project_id
        """,
        """
        CREATE VIEW workshop_schedule_view AS
        SELECT workshop_name, duration, about
        FROM workshops
        """
    ]

    con = connect_to_database()
    cursor = con.cursor()
    try:
        for view in views:
            cursor.execute(view)
            # Split the view string by " AS "
            view_parts = view.split(" AS ")
            # Check if the split operation produced at least two parts
            if len(view_parts) >= 2:
                print("View created successfully:", view_parts[1].split("\n")[0])
            else:
                print("Error: Unable to extract view name from the query:", view)
    except mysql.connector.Error as err:
        print("Error creating view:", err)
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    create_views()
