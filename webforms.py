from flask_wtf import FlaskForm # pip install flask_wtf
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea



# Create A Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()]) # In navbar we call this name="searched" so this is why we say searched
    submit = SubmitField("Submit")
    

# Create Login Form

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    

# Create a Post Form

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

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
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="Passwords must match!")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    