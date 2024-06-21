from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#Creating flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "super secret key"


# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("Enter Name: ", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
# FIELDS!!!
# BooleanField
# DateField
# DateTimeField
# DecimalField
# FileField
# HiddenField
# MultipleField
# FieldList
# FloatField
# FormField
# IntegerField
# PasswordField
# RadioField
# SelectField
# SelectMultipleField
# SubmitField
# StringField
# TextArea Field

# VALIDATORS
# DataRequired
# Email
# EqualTo
# InputRequired
# IPAddress
# Length
# MacAddress
# NumberRange
# Optional
# Regexp
# URL
# UUID
# AnyOf
# None Of

# Creating a route decorator
# @app.route('/')
# def index():
#     return '<h1>Hello World</h1>'

# FILTERS!!!
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags

@app.route('/')
def index():
    first_name = "john"
    # stuff = "this is <strong>Bold</strong> text"
    stuff = "This is bold text"
    favorite_pizza = ["Pepperoni", "Margarita", "Cheese", 41]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)

#localhost:5000/user/john
@app.route('/user/<name>')
def user(name): # passing name from above
    return render_template("user.html", user_name=name)

# my tries
# @app.route('/user/<user>/<system>')
# def save(user, system):
#     return f"<h1>Hello {user}, welcome to the {system}."

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