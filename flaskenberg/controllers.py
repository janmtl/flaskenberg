from flaskenberg import app, db
from flaskenberg.models import User, Task, Question, Choice, Answer, Survey

import flask.ext.sqlalchemy
from sqlalchemy.sql import and_, func
import hashlib, uuid
from flask import jsonify

def new_user(data=None, **kw):
  next_id = db.session.query(func.max(User.id)).first()[0]
  if (next_id == None):
    next_id = 0
  salt = uuid.uuid4().hex
  data['hash_id'] = hashlib.sha1(str(next_id+1) + salt).hexdigest()
  data['tally'] = 0
  pass

# NEW PROBLEM, I'M REASSIGNING THE SAME USER TO THE SAME TASKS

def assign_tasks(result=None, **kw):
  user_id = result['id']
  tasks = Task.query.filter(Task.tally < app.config['TASK_COMPLETED_TALLY']).limit(app.config['TASKS_PER_USER'])
  for task in tasks:
    surveys = Survey.query.filter_by(task_id=task.id)
    for survey in surveys:
      new_task = Answer(user_id = user_id, task_id = task.id, question_id = survey.question_id)
      db.session.add(new_task)
  db.session.commit()
  pass

def tally_task_and_user(result=None, **kw):
  task = Task.query.filter_by(id = result['task_id']).first()
  user = User.query.filter_by(id = result['user_id']).first()

  num_answers   = Answer.query.filter(and_(and_(Answer.user_id==result['user_id'], Answer.value!=None), Answer.task_id==result['task_id'])).count()
  num_questions = len(task.questions)
  print num_answers
  print num_questions

  if (num_answers == num_questions):
    task.tally = task.tally + 1
    user.tally = user.tally + 1
    db.session.commit();
  elif (num_answers > num_questions):
    print 'overcomplete task'
  pass

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(User,      methods=['GET', 'POST', 'PATCH'], 
                              include_columns=['id', 'hash_id', 'tally'], 
                              preprocessors={'POST': [new_user]}, 
                              postprocessors={'POST': [assign_tasks]})

manager.create_api(Task,      methods=['GET'], 
                              include_columns=['id', 'hash_id', 'title', 'content'])

manager.create_api(Question,  methods=['GET'], 
                              include_columns=['id', 'title', 'choices'])

manager.create_api(Choice,    methods=['GET'])

manager.create_api(Answer,    methods=['GET', 'PUT', 'PATCH'], 
                              include_columns=['id', 'user_id', 'task_id', 'question_id', 'value'],
                              postprocessors={'PUT_SINGLE': [tally_task_and_user]})

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/api/user/<int:user_id>/next')
def next(user_id):
  answer = Answer.query.filter(and_(Answer.user_id==user_id, Answer.value==None)).first()
  if (answer == None):
    result = {'id': user_id}
    assign_tasks(result)
    answer = Answer.query.filter(and_(Answer.user_id==user_id, Answer.value==None)).first()
  return jsonify(answer_id = answer.id, task_id = answer.task_id, question_id = answer.question_id)