import os
from flaskenberg import app, db

basedir = os.path.abspath(os.path.dirname(__file__))
dbdir = os.path.join(os.path.abspath(os.curdir), 'db/')
app.config['BASEDIR'] = basedir
app.config['SECRET_KEY'] = 'temporary_secret_key' # make sure to change this
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbdir + 'flaskenberg.db'

#How many users must answer a task before it's complete?
app.config['TASK_COMPLETED_TALLY'] = 2

#How many tasks must a user complete initially?
app.config['TASKS_PER_USER'] = 2