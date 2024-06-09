import sqlite3
import random

# Define skill levels
skill_levels = ['Novice', 'Advanced Beginner', 'Competent', 'Proficient', 'Expert']

# Create Project Management database
conn_pm = sqlite3.connect('project_management_database.db')
cursor_pm = conn_pm.cursor()

# Create Employees table in Project Management database
cursor_pm.execute('''
CREATE TABLE IF NOT EXISTS employees_pm (
    id INTEGER PRIMARY KEY,
    skills TEXT
)
''')

# Generate sample data for employees' skills with proficiency levels
skills_list = ['Python', 'Java', 'Data Analysis', 'Machine Learning', 'Project Management', 'SQL', 'JavaScript', 'C++', 'HTML', 'CSS']
employees_pm = []
for i in range(1, 51):
    num_skills = random.randint(1, 3)
    skills = ','.join([f"{skill}(Proficiency: {random.choice(skill_levels)})" for skill in random.sample(skills_list, num_skills)])
    employees_pm.append((i, skills))

cursor_pm.executemany('INSERT INTO employees_pm VALUES (?, ?)', employees_pm)

# Commit and close Project Management database
conn_pm.commit()
conn_pm.close()