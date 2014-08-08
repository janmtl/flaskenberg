from flaskenberg import app, db
from sqlalchemy.ext.associationproxy import association_proxy

questions_choices = db.Table('questions_choices',
  db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
  db.Column('choice_id',   db.Integer, db.ForeignKey('choice.id'))
)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  hash_id     = db.Column(db.Unicode, unique=True)
  gender      = db.Column(db.Unicode)
  age         = db.Column(db.Integer)
  tally       = db.Column(db.Integer)
  tasks       = association_proxy('answer', 'task')

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  hash_id     = db.Column(db.Unicode, unique=True)
  title       = db.Column(db.Unicode)
  content     = db.Column(db.Unicode)
  max_tally   = db.Column(db.Integer)
  questions   = association_proxy('survey', 'question')

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
  user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
  task_id     = db.Column(db.Integer, db.ForeignKey('task.id'))
  question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
  value       = db.Column(db.Unicode)
  timestamp   = db.Column(db.Unicode)
  ip_address  = db.Column(db.Unicode)
  user        = db.relationship(User,     backref='answer')
  task        = db.relationship(Task,     backref='answer')
  question    = db.relationship(Question, backref='answer')