from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///department.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    responsibilities = db.Column(db.Text, nullable=False)
    orders = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Person %r>' % self.id


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('index.html')


@app.route('/persons')
def persons():
    persons = Person.query.order_by(Person.date.desc()).all()
    return render_template('persons.html', persons=persons)


@app.route('/persons/<int:id>')
def person_detail(id):
    person = Person.query.get(id)
    return render_template('person_detail.html', person=person)


@app.route('/persons/<int:id>/del')
def person_delete(id):
    person = Person.query.get_or_404(id)

    try:
        db.session.delete(person)
        db.session.commit()
        return redirect('/persons')
    except:
        return 'Під час видалення трапилася помилка'


@app.route('/persons/<int:id>/update', methods=['POST', 'GET'])
def person_update(id):
    person = Person.query.get(id)
    if request.method == 'POST':
        person.firstName = request.form['firstName']
        person.lastName = request.form['lastName']
        person.bio = request.form['bio']
        person.position = request.form['position']
        person.responsibilities = request.form['responsibilities']
        person.orders = request.form['orders']

        try:
            db.session.commit()
            return redirect('/persons')
        except:
            return 'Під час видалення трапилася помилка'
    else:
        return render_template('person_update.html', person=person)


@app.route('/create_person', methods=['POST', 'GET'])
def create_person():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        bio = request.form['bio']
        position = request.form['position']
        responsibilities = request.form['responsibilities']
        orders = request.form['orders']

        person = Person(firstName=firstName, lastName=lastName, bio=bio, position=position, responsibilities=responsibilities, orders=orders)

        try:
            db.session.add(person)
            db.session.commit()
            return redirect('/persons')
        except:
            return 'Під час видалення трапилася помилка'
    else:
        return render_template('create_person.html')


if __name__ == '__main__':
    app.run(debug=True)
