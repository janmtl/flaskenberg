import os
from flaskenberg import app, db

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'temporary_secret_key' # make sure to change this
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/flaskenberg.db')
