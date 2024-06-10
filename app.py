from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///central_database.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employees_central'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    skills = db.Column(db.String(255))
    hours_remaining = db.Column(db.Integer)
    hours_worked = db.Column(db.Integer)
    utilization = db.Column(db.Float)
    previous_projects = db.Column(db.String(255))
    active_projects = db.Column(db.String(255))

    def __repr__(self):
        return f'<Employee {self.name}>'

@app.route('/')
def index():
    employees = Employee.query.order_by(Employee.utilization).all()
    return render_template('index.html', employees=employees)


@app.route('/filter', methods=['POST'])
def filter():
    name = request.form.get('name')
    skill = request.form.get('skill')
    hours_remaining = request.form.get('hours_remaining')
    utilization = request.form.get('utilization')
    proficiency = request.form.get('proficiency')

    query = Employee.query

    if name:
        query = query.filter(Employee.name.ilike(f'%{name}%'))
    if skill:
        query = query.filter(Employee.skills.ilike(f'%{skill}%'))
    if hours_remaining:
        query = query.filter(Employee.hours_remaining >= int(hours_remaining))
    if utilization:
        query = query.filter(Employee.utilization >= int(utilization) / 100)
    if proficiency:
        query = query.filter(Employee.skills.ilike(f'%({proficiency})%'))

    employees = query.order_by(Employee.utilization).all()

    return render_template('filter.html', employees=employees)


if __name__ == '__main__':
    app.run(debug=True)
