from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # pip install flask_login

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from webforms import LoginForm, PostForm, PasswordForm, NameForm, UserForm, SearchForm

from flask_ckeditor import CKEditor # pip install flask-ckeditor

from werkzeug.utils import secure_filename
import uuid as uuid
import os

#Creating flask instance
app = Flask(__name__)



# Add NoSql Database - old db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# MySql Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql1234@localhost/our_users' # pip install pymsysql and pip install cryptography

# app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://ufrlam7ksq0u44:p472be503258a48328a33137d4b459249c2d511dfcba7bd9d50f16da5c3bfc4ff@ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d9prtiib132cih'

# Secret Key
app.config['SECRET_KEY'] = "super secret key"

# Upload Image
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Add ckeditor
ckeditor = CKEditor(app)


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


# Pass Stuff To Navbar

@app.context_processor
def base():
    form = SearchForm() # Now this search form passed into base.html so navbar includes 
    return dict(form=form)


# Create Search Function

@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query # Searching content inside posts
    if form.validate_on_submit():
        # Get data from submitted form
        post.searched = form.searched.data
        # Query the database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        
        
        return render_template('search.html', 
            form=form,
            searched=post.searched,
            posts=posts)

# Flask Login Stuff

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create Login Page

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first() # First searchs for username if it exist. ( username is unique )
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull", "success")
                return redirect(url_for('dashboard'))     
            else:
                flash("Wrong Password Try Again", "danger")
        else:
            flash("This user does not exist!")
            
    return render_template('login.html', form=form)



# Create Logout Page

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!!")
    return redirect(url_for('login'))
 

# Create Dashboard Page

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.about_author = request.form['about_author']
        name_to_update.username = request.form['username']
        
        # Check for profile pic
        
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']
                    
            #Grab image name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename # Creating Unique filename
            
            # Save The Image
            saver = request.files['profile_pic']
            
            # Change it to a string to save to database
            name_to_update.profile_pic = pic_name
            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))    
                flash("User Updated Successfully!")

                return render_template("dashboard.html", 
                    form=form,
                    name_to_update=name_to_update)
            except:
                db.session.commit()
                flash("Error! ...try again")
                return render_template("dashboard.html", 
                    form=form,
                    name_to_update=name_to_update,
                    id=id)
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
            
    else:
        return render_template("dashboard.html", 
                form=form,
                name_to_update=name_to_update,
                id=id)
        



@app.route('/posts')
def posts():
    # Take all the posts from database
    
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


# Delete post

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    
    if id == post_to_delete.poster.id:    
        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            # Message
            flash('Blog Post Has Been Deleted!')
            
            # Take all the posts from database
        
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)

        except:
            # Error message
            flash("There was a problem while deleting..")
            
            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)

    else:
        flash("You Aren't Authorized To Delete!", "warning")
        
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)



# Edit post

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    
    if form.validate_on_submit():        
        post.title=form.title.data,
        post.content=form.content.data,
        # post.author=form.author.data,
        post.slug=form.slug.data

        # Update database
        db.session.add(post)
        db.session.commit()
        
        flash("Post Has Been Updated!")
        return redirect(url_for('post', id=post.id))

    if current_user.id == post.poster_id:
        # Putting previous data to see in the form before change
        form.title.data = post.title
        form.content.data = post.content
        # form.author.data = post.author
        form.slug.data = post.slug
        return render_template('edit_post.html', form=form)
    else:
        flash("You Aren't Authorized To Access This Page")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
    

# individual blog page

@app.route('/post/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)


# Add Post Page

@app.route('/add-post', methods=['GET', 'POST'])
# @login_required # Second way to do  is go to add_post.html
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            poster_id=poster,
            slug=form.slug.data)
        
        # After clear the form
        
        form.title.data = ''
        form.content.data = ''
        # form.author.data = ''
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


with app.app_context():
    db.create_all()



@app.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete(id):
    if id == current_user.id:
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
    else:
        flash("Sorry You Can't Delete This User...", "danger")
        return redirect(url_for('dashboard'))
        
    
# Update Database Record
@app.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        
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
                name_to_update=name_to_update,
                id=id)
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
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(username = form.username.data,
                         name=form.name.data,
                         email=form.email.data,
                         favorite_color=form.favorite_color.data,
                         password_hash=hashed_pw) # instead of password_hash=form.password_hash.data
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        
    our_users = Users.query.order_by(Users.date_added)                
    return render_template("add_user.html", 
        form=form,
        name=name,
        our_users=our_users)
    
    
# Admin Page

@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("Sorry You Must Be The Admin To Access This Page.")
        return redirect(url_for('dashboard'))

# Home Page    

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
    
    

# Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
   
    # Foreign Key to Link Users (refer to primary key of the user)

    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True) # flask db migrate -m "added username", flask db  upgrade
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text, nullable=True) #Text(500) # Added About Author Section // Add TextAreaField // Made a changes in database need to make migration
    profile_pic = db.Column(db.String(120), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Do password
    password_hash = db.Column(db.String(128))
    
    # User Can Have Many Posts
    posts = db.relationship('Posts', backref='poster') # flask db migrate -m 'add foreign key' # flask db upgrade
    
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


if __name__ == "__main__":
    app.run(debug=True)