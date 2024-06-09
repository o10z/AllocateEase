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
    availability = db.Column(db.Integer)
    hours_worked = db.Column(db.Integer)
    utilization = db.Column(db.Float)

    def __repr__(self):
        return f'<Employee {self.name}>'

@app.route('/')
def index():
    employees = Employee.query.order_by(Employee.utilization.asc()).all()
    return render_template('index.html', employees=employees)

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        name = request.form.get('name')
        skill = request.form.get('skill')
        availability = request.form.get('availability')
        utilization = request.form.get('utilization')
        proficiency = request.form.get('proficiency')

        query = Employee.query
        if name:
            query = query.filter(Employee.name.contains(name))
        if skill:
            query = query.filter(Employee.skills.contains(skill))
        if availability:
            query = query.filter(Employee.availability >= int(availability))
        if utilization:
            query = query.filter(Employee.utilization < float(utilization))
        if proficiency:
            query = query.filter(Employee.skills.contains(f'(Proficiency: {proficiency})'))

        employees = query.order_by(Employee.utilization.asc()).all()
        return render_template('filter.html', employees=employees)
    return render_template('filter.html', employees=[])

if __name__ == '__main__':
    app.run(debug=True)