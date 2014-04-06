import os
import flask
import flask.ext.sqlalchemy
import flask.ext.restless

basedir = os.path.abspath(os.path.dirname(__file__))
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/flaskenberg.db')
db = flask.ext.sqlalchemy.SQLAlchemy(app)

users_tasks = db.Table('users_tasks',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash_id = db.Column(db.Unicode, unique=True)
    gender = db.Column(db.Unicode)
    age = db.Column(db.Integer)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash_id = db.Column(db.Unicode, unique=True)
    users = db.relationship('User', secondary=users_tasks , backref=db.backref('tasks', lazy='dynamic'))

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(User, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Task, methods=['GET'])

# start the flask loop
app.run()