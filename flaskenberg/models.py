from flaskenberg import app, db

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