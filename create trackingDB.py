import sqlite3
from faker import Faker
import random



# Create Time Tracking database
conn_tt = sqlite3.connect('time_tracking_database.db')
cursor_tt = conn_tt.cursor()

# Create Employees table in Time Tracking database
cursor_tt.execute('''
CREATE TABLE IF NOT EXISTS employees_tt (
    id INTEGER PRIMARY KEY,
    total_availability INTEGER,
    hours_worked INTEGER,
    hours_remaining INTEGER
)
''')

# Generate random availability and hours worked, and calculate utilization
employees_tt = []
for i in range(1, 51):
    total_availability = random.randint(30, 50)
    hours_worked = random.randint(0, total_availability)
    hours_remaining = total_availability - hours_worked

    employees_tt.append((i, total_availability, hours_worked, hours_remaining))


cursor_tt.executemany('INSERT INTO employees_tt VALUES (?, ?, ?, ?)', employees_tt)

# Commit and close Time Tracking database
conn_tt.commit()
conn_tt.close()


