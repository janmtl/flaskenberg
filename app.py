import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import flask.ext.sqlalchemy
import flask.ext.restless

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder='static', static_url_path='')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/flaskenberg.db')
db = flask.ext.sqlalchemy.SQLAlchemy(app)

def init_api():
  users_tasks = db.Table('users_tasks',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
  )
  questions_tasks = db.Table('questions_tasks',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
  )
  questions_choices = db.Table('questions_choices',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
    db.Column('choice_id', db.Integer, db.ForeignKey('choice.id'))
  )

  class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash_id     = db.Column(db.Unicode, unique=True)
    gender      = db.Column(db.Unicode)
    age         = db.Column(db.Integer)
    count       = db.Column(db.Integer)

  class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash_id     = db.Column(db.Unicode, unique=True)
    title       = db.Column(db.Unicode)
    content     = db.Column(db.Unicode)
    complete    = db.Column(db.Boolean)
    users       = db.relationship('User', secondary=users_tasks, backref=db.backref('tasks', lazy='dynamic'))
    questions   = db.relationship('Question', secondary=questions_tasks)

  class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.Unicode)
    choices     = db.relationship('Choice', secondary=questions_choices)

  class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content     = db.Column(db.Unicode)
    value       = db.Column(db.Unicode)

  class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer)
    task_id     = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    value       = db.Column(db.Unicode)
    timestamp   = db.Column(db.DateTime)
    ip_address  = db.Column(db.Unicode)

  # Create the database tables.
  db.create_all()

  # Create the Flask-Restless API manager.
  manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

  # Create API endpoints, which will be available at /api/<tablename>
  manager.create_api(User,     methods=['GET', 'PUT', 'POST', 'DELETE'])
  manager.create_api(Task,     methods=['GET', 'PUT', 'POST', 'DELETE'])
  manager.create_api(Question, methods=['GET', 'PUT', 'POST', 'DELETE'])
  manager.create_api(Choice,   methods=['GET', 'PUT', 'POST', 'DELETE'])
  manager.create_api(Answer,   methods=['GET', 'PUT', 'POST', 'DELETE'])

@app.route('/')
def root():
  return app.send_static_file('index.html')

#@app.route('/<path:filename>')
#def statics(filename):
#    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
  init_api()
  app.run()
