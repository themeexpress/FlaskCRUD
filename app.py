
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# App secret
app.secret_key = 'mysecretofapps23453'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:123456@localhost/flaskcrud"
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Make model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))

    def __int__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


@app.route('/', methods=['POST', 'GET'])
def index():
    all_employees = Data.query.all()
    return render_template('index.html', employees=all_employees)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name=name, email=email, phone=phone)
        db.session.add(my_data)
        db.session.commit()
        # Flash message
        flash('Employee is inserted successfully', 'success')
        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        update_employee_data = Data.query.get(request.form.get('id'))
        update_employee_data.name = request.form['name']
        update_employee_data.email = request.form['email']
        update_employee_data.phone = request.form['phone']
        db.session.commit()

        # Flash message
        flash('Employee is updated successfully', 'success')
        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    delete_employee_data = Data.query.get(id)
    db.session.delete(delete_employee_data)
    db.session.commit()

    # Flash message
    flash('Employee is deleted successfully', 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

