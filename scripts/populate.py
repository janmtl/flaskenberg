import os
import sys
import flask.ext.sqlalchemy
from flaskenberg import app, db

if __name__ == '__main__':
  db.metadata.drop_all(db.engine)
  db.create_all()
  seed = open(os.path.join(os.path.abspath(os.curdir), 'db/data.sql'))
  for line in seed:
    if line[0]!='#':
      db.engine.execute(line)