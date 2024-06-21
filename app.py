from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Creating flask instance
app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY'] = "super secret key"

# Initialize Database

db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A string
    def __repr__(self):
        return '<Name %r>' % self.name

with app.app_context():
    db.create_all()

# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("Enter Name: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added successfully!")
        
    our_users = Users.query.order_by(Users.date_added)                
    return render_template("add_user.html", 
        form=form,
        name=name,
        our_users=our_users)
    
    
    
    
@app.route('/')
def index():
    first_name = "john"
    stuff = "This is bold text"
    # flash("Welcome to flask website!")
 
    favorite_pizza = ["Pepperoni", "Margarita", "Cheese", 41]
    return render_template("index.html",
        first_name=first_name,
        stuff=stuff,
        favorite_pizza=favorite_pizza)
    
    
#localhost:5000/user/john
@app.route('/user/<name>')
def user(name): # passing name from above
    return render_template("user.html", user_name=name)


# Create Custom Error Pages

#1-Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#2-Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Create Name Page
@app.route("/name", methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
        
    return render_template("name.html",
        name=name,
        form=form)



if __name__ == "__main__":
    app.run(debug=True)