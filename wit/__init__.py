import os

from datetime import datetime
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

from wit.models import Case, Witness, Code, Statement, Entity, EntityStatement
from wit.nlp import process_text

import wit.witness
import wit.police
