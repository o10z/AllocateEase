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
    availability INTEGER,
    hours_worked INTEGER
)
''')

# Generate random availability and hours worked, and calculate utilization
employees_tt = []
for i in range(1, 51):
    availability = random.randint(20, 40)
    hours_worked = random.randint(0, availability)
    employees_tt.append((i, availability, hours_worked))

cursor_tt.executemany('INSERT INTO employees_tt VALUES (?, ?, ?)', employees_tt)

# Commit and close Time Tracking database
conn_tt.commit()
conn_tt.close()


