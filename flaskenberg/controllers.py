from flaskenberg import app, db
from flaskenberg.models import User, Task, Question, Choice, Answer
import flask.ext.sqlalchemy
from sqlalchemy.sql import and_
from flask import jsonify

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(User,     methods=['GET', 'POST', 'PATCH'], include_columns=['id', 'hash_id', 'count'])
manager.create_api(Task,     methods=['GET'], include_columns=['id', 'hash_id', 'title', 'content'])
manager.create_api(Question, methods=['GET'], include_columns=['id', 'title', 'choices'])
manager.create_api(Choice,   methods=['GET'])
manager.create_api(Answer,   methods=['GET', 'PUT', 'POST', 'PATCH'], include_columns=['id', 'user_id', 'task_id', 'question_id', 'value'])

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/api/user/<int:user_id>/next')
def next(user_id):
  answer = Answer.query.filter(and_(Answer.user_id==user_id, Answer.value=='')).first()
  return jsonify(answer_id = answer.id, task_id = answer.task_id, question_id = answer.question_id)

#@app.route('/<path:filename>')
#def statics(filename):
#    return send_from_directory(app.static_folder, filename)

