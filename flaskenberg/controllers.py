from flaskenberg import app, db
from flaskenberg.models import User, Task, Question, Choice, Answer
import flask.ext.sqlalchemy
from flask import jsonify

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(User,     methods=['GET', 'POST', 'PATCH'], include_columns=['id', 'hash_id', 'tasks', 'count'])
manager.create_api(Task,     methods=['GET'])
manager.create_api(Question, methods=['GET'])
manager.create_api(Choice,   methods=['GET'])
manager.create_api(Answer,   methods=['GET', 'POST', 'PATCH'], include_columns=['id', 'user_id', 'task_id', 'question_id', 'value'])

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/api/user/<int:user_id>/next')
def next_task(user_id):
  user = User.query.filter_by(id=user_id).first()
  return jsonify(task_id = user.tasks[user.count].id)

#@app.route('/<path:filename>')
#def statics(filename):
#    return send_from_directory(app.static_folder, filename)

