from flask import Flask
from peewee import SqliteDatabase

app = Flask(__name__)
app.config.from_object('wit.config')
db = SqliteDatabase(app.config['DATABASE'])

def init_db():
    db.connect()
    db.create_tables()

import wit.models
import wit.backend
