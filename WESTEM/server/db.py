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


#creating databse

"""
cursor.execute("CREATE DATABASE westem")
cursor.execute("SHOW DATABASES")

for db in cursor:
    print (db)
"""


#Queries for table creation
create_table_users = """
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
    address VARCHAR(100),
    career_status VARCHAR(50),
    dob DATE,
    password VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20)
);
"""

# Execute the SQL statement to create the table
cursor.execute(create_table_users)


create_table_employee = """
CREATE TABLE IF NOT EXISTS employee (
    employer_id INTEGER PRIMARY KEY NOT NULL,
    password VARCHAR(50),
    email VARCHAR(100),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATE,
    address VARCHAR(100),
    phone_number VARCHAR(20),
    experience TEXT
);
"""


# Execute the SQL statement to create the table
cursor.execute(create_table_employee)

create_project_query = """
CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY NOT NULL,
    budget DECIMAL,
    type VARCHAR(50),
    name VARCHAR(100),
    user_id VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(username)
);
"""

# Execute the SQL statement to create the project table
cursor.execute(create_project_query)

# Define SQL statement to create the mentorship table
create_mentorship_table_query = """
CREATE TABLE IF NOT EXISTS mentorship (
    user_id VARCHAR(50),
    project_id INTEGER,
    employee_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(username),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employer_id),
    PRIMARY KEY (user_id, project_id, employee_id)
);
"""

# Execute the SQL statement to create the mentorship table
cursor.execute(create_mentorship_table_query)


# Define SQL statement to create the resources table (superclass)
create_resources_query = """
CREATE TABLE IF NOT EXISTS resources (
    resource_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    employee_id INTEGER UNIQUE,
    FOREIGN KEY (employee_id) REFERENCES employee(employer_id)
);
"""

# Define SQL statement to create the workshops table (subclass)
create_workshops_query = """
CREATE TABLE IF NOT EXISTS workshops (
    resource_id INTEGER PRIMARY KEY,
    duration INTEGER,
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id)
);
"""

# Define SQL statement to create the resume_review table (subclass)
create_resume_review_query = """
CREATE TABLE IF NOT EXISTS resume_review (
    resource_id INTEGER PRIMARY KEY,
    reviewer VARCHAR(100),
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id)
);
"""

# Define SQL statement to create the mentorship_program table (subclass)
create_mentorship_program_query = """
CREATE TABLE IF NOT EXISTS mentorship_program (
    resource_id INTEGER PRIMARY KEY,
    mentor VARCHAR(100),
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id)
);
"""

# Execute the SQL statements to create the tables
cursor.execute(create_resources_query)
cursor.execute(create_workshops_query)
cursor.execute(create_resume_review_query)
cursor.execute(create_mentorship_program_query)


# Define SQL statement to create the documents table
create_documents_table_query = """
CREATE TABLE IF NOT EXISTS documents (
    document_id INTEGER PRIMARY KEY NOT NULL,
    title VARCHAR(100),
    type VARCHAR(50),
    filename VARCHAR(100),
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(username)
);
"""

# Execute the SQL statement to create the documents table
cursor.execute(create_documents_table_query)


# Define SQL statement to create the resource_application table
create_resource_application_table_query = """
CREATE TABLE IF NOT EXISTS resource_application (
    user_id VARCHAR(50),
    resource_id INTEGER,
    document_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(username),
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id),
    FOREIGN KEY (document_id) REFERENCES documents(document_id),
    PRIMARY KEY (user_id, resource_id, document_id)
);
"""

# Execute the SQL statement to create the resource_application table
cursor.execute(create_resource_application_table_query)
con.commit()