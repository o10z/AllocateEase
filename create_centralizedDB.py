import sqlite3

# Create Centralized database and populate it
conn_central = sqlite3.connect('instance/central_database.db')
cursor_central = conn_central.cursor()

cursor_central.execute('''
CREATE TABLE IF NOT EXISTS employees_central (
    id INTEGER PRIMARY KEY,
    name TEXT,
    skills TEXT,
    total_availability INTEGER,
    hours_remaining INTEGER,
    hours_worked INTEGER,
    utilization REAL,
    previous_projects TEXT,
    active_projects TEXT
)
''')

# Extract and insert data into Centralized database
def extract_and_insert():
    conn_hr = sqlite3.connect('hr_database.db')
    cursor_hr = conn_hr.cursor()
    conn_pm = sqlite3.connect('project_management_database.db')
    cursor_pm = conn_pm.cursor()
    conn_tt = sqlite3.connect('time_tracking_database.db')
    cursor_tt = conn_tt.cursor()

    cursor_hr.execute('SELECT id, name FROM employees_hr')
    employees_hr_data = cursor_hr.fetchall()

    cursor_pm.execute('SELECT id, skills, previous_projects, active_projects FROM employees_pm')
    employees_pm_data = cursor_pm.fetchall()

    cursor_tt.execute('SELECT id, total_availability, hours_worked, hours_remaining FROM employees_tt')
    employees_tt_data = cursor_tt.fetchall()

    conn_hr.close()
    conn_pm.close()
    conn_tt.close()

    pm_data_map = {emp[0]: emp[1:] for emp in employees_pm_data}
    tt_data_map = {emp[0]: emp[1:] for emp in employees_tt_data}

    for emp in employees_hr_data:
        emp_id = emp[0]
        name = emp[1]
        pm_data = pm_data_map.get(emp_id, (None, None, None))
        skills = pm_data[0]
        previous_projects = pm_data[1]
        active_projects = pm_data[2]
        tt_data = tt_data_map.get(emp_id, (None, None))
        total_availability, hours_worked, hours_remaining = tt_data
        utilization = round(hours_worked / total_availability, 2) if total_availability else None
        cursor_central.execute('''
            INSERT INTO employees_central (id, name, skills, hours_remaining, hours_worked, utilization,
             previous_projects, active_projects)
             
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (emp_id, name, skills, hours_remaining, hours_worked, utilization, previous_projects, active_projects))

    conn_central.commit()


extract_and_insert()
conn_central.close()
