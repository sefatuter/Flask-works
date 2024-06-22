# Flask-works
Flask App

in bash :

$ python -m venv venv
$ source venv/Scripts/activate
$ export FLASK_ENV=development
$ export FLASK_APP=app.py
$ flask run --debug


for mac :

$ export FLASK_ENV=development
$ flask run --debug


creating db in bash :

$ flask shell
>>> from app import db
>>> db.create_all()
