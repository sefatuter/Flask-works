from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Creating flask instance
app = Flask(__name__)

# Add NoSql Database - old db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# MySql Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql1234@localhost/our_users' # pip install pymsysql and pip install cryptography


# Secret Key
app.config['SECRET_KEY'] = "super secret key"

# Initialize Database

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# $ flask db init
# to create migrations and then,
# $ flask db migrate -m 'Initial Migration'
# its using for new added column to push database then, ( we added favorite color to code )
# $ flask db upgrade
# $ flask run --debug
# and then we can see the new changes...

# after you created migration environment
# to make changes use,
# $ flask db migrate -m "message"
# $ flask db upgrade

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
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
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")
    

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    name = None
    form = UserForm()
    user_to_delete = Users.query.get_or_404(id)
   
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        
        our_users = Users.query.order_by(Users.date_added)                
        return render_template("add_user.html", 
        form=form,
        name=name,
        our_users=our_users)
    except:
        flash("Whoops! There was a problem...")
        return render_template("add_user.html", 
        form=form,
        name=name,
        our_users=our_users)
        
        
    
# Update Database Record
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")

            return render_template("update.html", 
                form=form,
                name_to_update=name_to_update)
        except:
            db.session.commit()
            flash("Error! ...try again")
            return render_template("update.html", 
                form=form,
                name_to_update=name_to_update)
    else:
        return render_template("update.html", 
                form=form,
                name_to_update=name_to_update,
                id=id)
    
    
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        
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
        
    return render_template("name.html",
        name=name,
        form=form)



if __name__ == "__main__":
    app.run(debug=True)