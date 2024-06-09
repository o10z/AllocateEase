import sqlite3

# Create Centralized database and populate it
conn_central = sqlite3.connect('instance/central_database.db')
cursor_central = conn_central.cursor()

cursor_central.execute('''
CREATE TABLE IF NOT EXISTS employees_central (
    id INTEGER PRIMARY KEY,
    name TEXT,
    skills TEXT,
    availability INTEGER,
    hours_worked INTEGER,
    utilization REAL
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

    cursor_pm.execute('SELECT id, skills FROM employees_pm')
    employees_pm_data = cursor_pm.fetchall()

    cursor_tt.execute('SELECT id, availability, hours_worked FROM employees_tt')
    employees_tt_data = cursor_tt.fetchall()

    conn_hr.close()
    conn_pm.close()
    conn_tt.close()

    pm_data_map = {emp[0]: emp[1] for emp in employees_pm_data}
    tt_data_map = {emp[0]: emp[1:] for emp in employees_tt_data}

    for emp in employees_hr_data:
        emp_id = emp[0]
        name = emp[1]
        skills = pm_data_map.get(emp_id, None)
        availability, hours_worked = tt_data_map.get(emp_id, (None, None))
        utilization = round(hours_worked / availability, 2) if availability else None
        cursor_central.execute('''
            INSERT INTO employees_central (id, name, skills, availability, hours_worked, utilization)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (emp_id, name, skills, availability, hours_worked, utilization))

    conn_central.commit()


extract_and_insert()
conn_central.close()