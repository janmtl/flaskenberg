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

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  hash_id     = db.Column(db.Unicode, unique=True)
  title       = db.Column(db.Unicode)
  content     = db.Column(db.Unicode)
  repetitions = db.Column(db.Integer)
  task2answer = db.relationship('Answer', primaryjoin="and_(Task.id==Answer.task_id, Answer.user_id==0)", uselist=True)
  questions   = association_proxy('task2answer', 'question')

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
  user        = db.relationship(User)
  task        = db.relationship(Task)
  question    = db.relationship(Question)

  @property
  def serialize(self):
     return {
         'id'          : self.id,
         'user_id'     : self.user_id,
         'task_id'     : self.task_id,
         'question_id' : self.question_id,
         'value'       : self.value
     }