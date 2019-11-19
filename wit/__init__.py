from flask import Flask
from jinja2 import Environment, FileSystemLoader, select_autoescape
from peewee import SqliteDatabase

app = Flask(__name__)
app.config.from_object('wit.config')
env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape = select_autoescape(['html', 'css'])
        )
db = SqliteDatabase(app.config['DATABASE'])

def init_db():
    db.connect()
    db.create_tables()

import wit.models
import wit.witness
import wit.backend
