import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Create Centralized database and populate it
conn_central = sqlite3.connect('instance/central_database.db')
cursor_central = conn_central.cursor()

# Create employees_table
cursor_central.execute('''
    CREATE TABLE IF NOT EXISTS employees_table (
        EmployeeID INTEGER PRIMARY KEY,
        Name TEXT,
        JobTitle TEXT,
        Department TEXT,
        DateOfJoining TEXT,
        EmploymentType TEXT,
        WorkSchedule INTEGER,
        ContactInfo TEXT
    )
''')

# Create skills_table
cursor_central.execute('''
    CREATE TABLE IF NOT EXISTS skills_table (
        SkillID INTEGER PRIMARY KEY,
        EmployeeID INTEGER,
        SkillName TEXT,
        ProficiencyLevel TEXT,
        LastUpdated DATETIME
    )
''')

# Create projects_table
cursor_central.execute('''
    CREATE TABLE IF NOT EXISTS projects_table (
        ProjectID INTEGER PRIMARY KEY,
        ProjectName TEXT,
        StartDate DATETIME,
        EndDate DATETIME,
        Status TEXT,
        Description TEXT
    )
''')

# Create EmployeeProjects_table
cursor_central.execute('''
    CREATE TABLE IF NOT EXISTS EmployeeProjects_table (
        EmployeeID INTEGER,
        ProjectID INTEGER,
        Role TEXT,
        TimeAllocated INTEGER
    )
''')

# Generate random data for employees_table
employees = []
for _ in range(10):
    employee = (
        None,
        fake.name(),
        random.choice(["Software Developer", "Project Manager", "Office manager", "UX designer", "UI developer",
                       "IT manager", "Data architect", "Software engineer", "Database manager"]),
        "IT",
        fake.date_this_decade(),
        random.choice(["Full-time", "Part-time", "Contract"]),
        random.randint(30, 40),  # Work schedule in hours per week
        fake.email()
    )
    employees.append(employee)

cursor_central.executemany("INSERT INTO employees_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)", employees)

# Generate random data for skills_table
skills = []
for i in range(1, 11):
    for _ in range(random.randint(1, 3)):  # Each employee has between 1 and 3 skills
        skill = (
            None,
            i,
            random.choice(['Python', 'Java', 'Data Analysis', 'Machine Learning', 'Project Management', 'SQL',
                           'JavaScript', 'C++', 'HTML', 'CSS']),
            random.choice(["Beginner", "Intermediate", "Proficient", "Expert"]),
            fake.date_this_year()
        )
        skills.append(skill)

cursor_central.executemany("INSERT INTO skills_table VALUES (?, ?, ?, ?, ?)", skills)

# Generate random data for projects_table
projects = []
for _ in range(20):
    start_date = fake.date_this_decade()
    end_date = start_date + timedelta(days=random.randint(30, 365))
    project = (
        None,
        fake.bs(),
        start_date,
        end_date,
        random.choice(["Completed", "In Progress", "Pending"]),
        fake.text()
    )
    projects.append(project)

cursor_central.executemany("INSERT INTO projects_table VALUES (?, ?, ?, ?, ?, ?)", projects)

# Generate random data for EmployeeProjects_table
employee_projects = []
for i in range(1, 51):
    for _ in range(random.randint(1, 3)):  # Each employee is assigned to between 1 and 3 projects
        employee_project = (
            i,
            random.randint(1, 20),  # Assuming 20 projects exist
            random.choice(["Manager", "Developer", "Analyst", "Consultant"]),
            random.randint(20, 40)  # Time allocated in hours per week
        )
        employee_projects.append(employee_project)

cursor_central.executemany("INSERT INTO EmployeeProjects_table VALUES (?, ?, ?, ?)", employee_projects)

# Commit changes and close connection
conn_central.commit()
conn_central.close()