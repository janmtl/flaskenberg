from flaskenberg import app, db
from flaskenberg.models import User, Task, Question, Choice, Answer
import flask.ext.sqlalchemy

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(User,     methods=['GET', 'POST', 'PATCH'])
manager.create_api(Task,     methods=['GET'])
manager.create_api(Question, methods=['GET'])
manager.create_api(Choice,   methods=['GET'])
manager.create_api(Answer,   methods=['GET', 'POST', 'PATCH'])

@app.route('/')
def root():
  return app.send_static_file('index.html')

#@app.route('/<path:filename>')
#def statics(filename):
#    return send_from_directory(app.static_folder, filename)

