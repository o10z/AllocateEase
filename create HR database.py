import sqlite3
from faker import Faker

fake = Faker()

# Create HR database
conn_hr = sqlite3.connect('hr_database.db')
cursor_hr = conn_hr.cursor()

# Create Employees table in HR database
cursor_hr.execute('''
CREATE TABLE IF NOT EXISTS employees_hr (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date_of_birth TEXT,
    address TEXT,
    contact_number TEXT
)
''')

# Generate sample data for 50 employees
employees_hr = [(i, fake.name(), fake.date_of_birth(minimum_age=20, maximum_age=60).isoformat(), fake.address(), fake.phone_number()) for i in range(1, 51)]
cursor_hr.executemany('INSERT OR IGNORE INTO employees_hr VALUES (?, ?, ?, ?, ?)', employees_hr)

# Commit and close HR database
conn_hr.commit()
conn_hr.close()