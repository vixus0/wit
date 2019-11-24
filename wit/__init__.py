from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from jinja2 import Environment, FileSystemLoader, select_autoescape
from peewee import SqliteDatabase

app = Flask(__name__)
app.config.from_object('wit.config')
env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape = select_autoescape(['html', 'css'])
        )
db = SqliteDatabase(app.config['DATABASE'])

from wit.models import Case, Witness, Code, Statement
from wit.nlp import process_text

with db:
    db.create_tables([Case, Witness, Code, Statement])
    case = Case.create(name='Sample Case')

    witness1 = Witness.create(case=case, name='Alan Smith', postcode='DE1 2EA', mobile='01234567890')
    code1 = Code.create(witness=witness1, used=datetime.now())
    text1 = '''
    I saw a murder in Overton Park.
    '''
    doc1 = process_text(text1).to_bytes()
    statement1 = Statement.create(code=code1, supervised=True, text=text1, spacy_doc=doc1)

    witness2 = Witness.create(case=case, name='Becky Parks', mobile='01234788961', email='becky.parks@example.com')
    code2 = Code.create(witness=witness1, used=datetime.now())
    text2 =  '''
    There was an attack in Overton Park by the swings.
    I think I recognised Jim Burns from down the road.
    '''
    doc2 = process_text(text1).to_bytes()
    statement2 = Statement.create(code=code1, supervised=True, text=text1, spacy_doc=doc1)

import wit.witness
import wit.backend
