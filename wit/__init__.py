import os

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

from wit.models import Case, Witness, Code, Statement, Entity, EntityStatement
from wit.nlp import process_text

def create_statement(case, code, text, supervised=False):
    doc = process_text(text)
    statement = Statement.create(code=code, case=case, text=text, supervised=supervised, spacy_doc=doc.to_bytes())
    entity_data = set()
    entity_statement_data = list()
    for ent in doc.ents:
        entity_id = f'{ent.label_}__{ent.text}'.lower().replace(' ','_')
        entity_data.add((entity_id, ent.label_, ent.text))
        entity_statement_data.append((entity_id, statement.id))
    Entity.insert_many(entity_data, fields=[Entity.id, Entity.label, Entity.text]).on_conflict_ignore().execute()
    EntityStatement.insert_many(entity_statement_data, fields=[EntityStatement.entity, EntityStatement.statement]).execute()
    return statement

if not os.path.exists(app.config['DATABASE']):
    with db.atomic():
        db.create_tables([Case, Witness, Code, Statement, Entity, EntityStatement])
        case = Case.create(name='Sample Case')

        witness1 = Witness.create(case=case, name='Alan Smith', postcode='DE1 2EA', mobile='01234567890')
        code1 = Code.create(witness=witness1, used=datetime.now())
        text1 = '''
        I saw a murder in Overton Park.
        '''
        statement1 = create_statement(case, code1, text1, supervised=True)

        witness2 = Witness.create(case=case, name='Becky Parks', mobile='01234788961', email='becky.parks@example.com')
        code2 = Code.create(witness=witness2, used=datetime.now())
        text2 =  '''
        There was an attack in Overton Park by the swings.
        I think I recognised Jim Burns from down the road.
        '''
        statement2 = create_statement(case, code2, text2, supervised=True)

import wit.witness
import wit.police
