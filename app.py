from data import person_data, statement_data, persons_statements, statements_persons

from flask import Flask, escape, request
from jinja2 import Environment, FileSystemLoader, select_autoescape
from spacy import displacy

env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape = select_autoescape(['html'])
        )

app = Flask(__name__)

@app.route('/')
def list():
    _persons = { key:person['fullName'] for key, person in person_data.items() }
    _statements = { key:doc.user_data['title'] for key, doc in statement_data.items() }
    return env.get_template('list.html').render(persons=_persons, statements=_statements)

@app.route('/person/<id>')
def person(id):
    _person = person_data[id]
    _statements = { st : statement_data[st] for st in persons_statements[id] }
    return env.get_template('person.html').render(person=_person, statements=_statements)

@app.route('/statement/<id>')
def statement(id):
    _statement = statement_data[id]
    _persons = [ person_data[ps] for ps in statements_persons[id] ]
    _statement.user_data['title'] = _statement.user_data['title'].replace('-', ' ').title()
    _spacy_html = displacy.render(_statement, style='ent', minify=True)
    return env.get_template('statement.html').render(statement=_statement, ents=_spacy_html, persons=_persons)
