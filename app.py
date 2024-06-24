from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm # pip install flask_wtf
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from wtforms.widgets import TextArea
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


# if changes made in another computer use:
# $ flask db stamp head
# $ flask db migrate
# $ flask db upgrade

# Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))

# Create a Post Form

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/posts')
def posts():
    # Take all the posts from database
    
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


@app.route('/post/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)



# Add Post Page

@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data,
            slug=form.slug.data)
        
        # After clear the form
        
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        
        # Add post to database
        db.session.add(post)
        db.session.commit()
        
        flash("Blog Post Submitted Successfully!!")
        
        # Redirect to website
    return render_template("add_post.html", form=form)

# JSON

@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "John": "Pepperoni",
        "Mary": "Cheese",
        "Tim": "Mushroom"
    }
    return favorite_pizza
    # return {"Date": datetime.date.today()}


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Do password
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('Password is a not readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # $ flask shell
    # >>> from app import Users
    # >>> u = Users()
    # >>> u.password = 'cat'
    # >>> u.password
    # Traceback (most recent call last):
    #   File "<console>", line 1, in <module>
    #   File "/Users/afnesia/Desktop/GitHub/Flask-works/app.py", line 55, in password
    #     raise AttributeError('Password is a not readable attribute!')
    # AttributeError: Password is a not readable attribute!
    # >>> u.password_hash
    # 'pbkdf2:sha256:260000$7pTAAEhwrkrj3Ive$d3c72e04fd3cf56faea7276686407a7ab4150353e7e8cde0953936eecedee268'
    # >>> u.verify_password('cat)
    # True
    # >>> u.verify_password('dog')
    # False
    
    # >>> u2 = Users()
    # >>> u2.password = 'cat'
    # >>> u2.password_hash
    # 'pbkdf2:sha256:260000$G6dAVnLD92bn1V9S$0740c4598b58354a7eccf1cd6fa9236b2a6e2c36c0b57008d8a14665e2689791'
    
    # We need to make migration
    
    # Create A string
    def __repr__(self):
        return '<Name %r>' % self.name

with app.app_context():
    db.create_all()

# Create a Form Class
class PasswordForm(FlaskForm):
    email = StringField("Enter Email: ", validators=[DataRequired()])
    password_hash = PasswordField("Enter Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class NameForm(FlaskForm):
    name = StringField("Enter Name: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="Passwords must match!")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
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
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data,
                         email=form.email.data,
                         favorite_color=form.favorite_color.data,
                         password_hash=hashed_pw) # instead of password_hash=form.password_hash.data
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        
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


    
# Create Password Test Page
@app.route("/test_pw", methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''
        
        # Lookup user by email address
        pw_to_check = Users.query.filter_by(email=email).first()
        
        # Check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)
        
    return render_template("test_pw.html",
        email=email,
        password=password,
        pw_to_check=pw_to_check,
        passed=passed,
        form = form)
    

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