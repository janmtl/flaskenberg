from flaskenberg import app, db
from flaskenberg.models import User, Task, Question, Choice, Answer

import flask.ext.sqlalchemy
from sqlalchemy.sql import and_, or_, func
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

def notify_hash_id(result=None, **kw):
  user = User.query.filter_by(id = result['id']).first()
  result['hash_id'] = user.hash_id
  print result
  pass

def assign_task(result=None, **kw):
  user_id = result['id']

  # SELECT count(*)-1 AS tallies, task_id, question_id FROM answer 
  #   WHERE (value is not null OR user_id = 0)
  #   GROUP BY task_id, question_id
  tallies = Answer.query.\
            with_entities(Answer.task_id, Answer.question_id, func.count(Answer.user_id).label('tally')).\
            filter(or_(Answer.value == None, Answer.user_id == 0)).\
            group_by(Answer.task_id, Answer.question_id).\
            subquery()

  # SELECT id, repetitions FROM task
  repetitions = Task.query.\
                with_entities(Task.id, Task.repetitions).\
                subquery()

  #SELECT * FROM answer AS a
  #  LEFT JOIN(tallies) AS b ON a.task_id = b.task_id AND a.question_id = b.question_id
  #  JOIN(repetitions)  AS t ON a.task_id = t.id
  # WHERE a.user_id =18 OR a.user_id = 0
  # GROUP BY a.task_id, a.question_id
  # HAVING a.user_id !=18
  new_task = Answer.query.with_entities(Answer.task_id.label('id'), Answer.question_id).\
             outerjoin(tallies, and_(Answer.task_id == tallies.c.task_id, Answer.question_id == tallies.c.question_id)).\
             join(repetitions, Answer.task_id == repetitions.c.id).\
             filter(or_(Answer.user_id == user_id, Answer.user_id == 0)).\
             group_by(Answer.task_id, Answer.question_id).\
             having(and_(Answer.user_id != user_id, tallies.c.tally < repetitions.c.repetitions+1)).\
             first()
  
  if new_task==[]:
    pass
  else:
    questions = Answer.query.\
                with_entities(Answer.question_id.label('id')).\
                filter(and_(Answer.user_id == 0, Answer.task_id == new_task.id)).\
                all()

    for question in questions:
      new_answer = Answer(user_id = user_id, task_id = new_task.id, question_id = question.id)
      db.session.add(new_answer)
    db.session.commit()
  
  pass

def tally_user(result=None, **kw):
  user = User.query.filter_by(id = result['user_id']).first()
  num_answers = Answer.query.filter(and_(Answer.user_id==result['user_id'], Answer.value!=None)).count()
  user.tally = num_answers 
  db.session.commit();
  pass

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(User,      methods=['GET', 'POST', 'PATCH'], 
                              include_columns=['id', 'tally'], 
                              preprocessors={'POST': [new_user]},
                              postprocessors={'POST': [assign_task, notify_hash_id]})

manager.create_api(Task,      methods=['GET'], 
                              include_columns=['id', 'title', 'content', 'questions'])

manager.create_api(Question,  methods=['GET'], 
                              include_columns=['id', 'title', 'choices'])

manager.create_api(Choice,    methods=['GET'])

manager.create_api(Answer,    methods=['GET', 'PUT'], 
                              include_columns=['id', 'user_id', 'task_id', 'question_id', 'value'],
                              postprocessors={'PUT_SINGLE': [tally_user]})

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/api/user/<int:user_id>/next')
def next(user_id):
  # SELECT * FROM answer AS a
  # JOIN (SELECT user_id, min(task_id) AS task_id FROM answer WHERE user_id=user_id AND value is null) AS b
  # ON a.user_id=b.user_id AND a.task_id = b.task_id
  subquery = Answer.query.with_entities(Answer.user_id, func.min(Answer.task_id).label('task_id')).filter(and_(Answer.user_id == user_id, Answer.value == None)).subquery()
  answers  = Answer.query.join(subquery, and_(Answer.user_id==subquery.c.user_id, Answer.task_id==subquery.c.task_id)).all()

  if answers == []:
    result = {'id': user_id}
    assign_task(result)
    subquery = Answer.query.with_entities(Answer.user_id, func.min(Answer.task_id).label('task_id')).filter(and_(Answer.user_id == user_id, Answer.value == None)).subquery()
    answers  = Answer.query.join(subquery, and_(Answer.user_id==subquery.c.user_id, Answer.task_id==subquery.c.task_id)).all()

  objects  = [answer.serialize for answer in answers]
  if objects == []:
    task_id = 'NA'
    num_results = 0
  else:
    task_id  = objects[0]['task_id']
    num_results = len(objects)

  return jsonify(num_results = num_results, task_id = task_id, objects = objects)