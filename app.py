from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audience.db'
db = SQLAlchemy(app)

class AudienceDB(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    surname = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AudienceDB {self.name} {self.surname}>'

with app.app_context():
    db.create_all()

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        # return 'Hi'
        name = request.form['name']
        surname = request.form['surname']
        new_person = AudienceDB(name=name, surname=surname)
        
        try:
            db.session.add(new_person)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding person.'
            
    else:
        persons = AudienceDB.query.order_by(AudienceDB.date_created).all()
        return render_template('index.html', persons=persons)



if __name__ == "__main__":
    app.run(debug=True)