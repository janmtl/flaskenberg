from flask.ext.script import Manager
from flaskenberg import app, db
import os

manager = Manager(app)

@manager.command
def populate():
  "Populates the database with seed data for testing"
  db.metadata.drop_all(db.engine)
  db.create_all()
  seed = open(os.path.join(os.path.abspath(os.curdir), 'db/data.sql'))
  for line in seed:
    if line[0]!='#':
      db.engine.execute(line)

if __name__ == "__main__":
    manager.run()