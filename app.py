from flask import Flask, render_template

#Creating flask instance
app = Flask(__name__)


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