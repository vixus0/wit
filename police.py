#!/usr/bin/env python

from data import person_data, statement_data, persons_statements, statements_persons
from network import generate_json

from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader, select_autoescape
from spacy import displacy

generate_json()

env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape = select_autoescape(['html', 'css'])
        )

app = Flask(__name__)

@app.route('/')
def list():
    _persons = { key:person['fullName'] for key, person in person_data.items() }
    _statements = { key:doc.user_data['title'] for key, doc in statement_data.items() }
    return render_template('list.html', persons=_persons, statements=_statements)

@app.route('/person/<id>')
def person(id):
    _person = person_data[id]
    _statements = { st : statement_data[st] for st in persons_statements[id] }
    return render_template('person.html', person=_person, statements=_statements)

@app.route('/statement/<id>')
def statement(id):
    _statement = statement_data[id]
    _persons = [ person_data[ps] for ps in statements_persons[id] ]
    _statement.user_data['title'] = _statement.user_data['title'].replace('-', ' ').title()
    _spacy_html = displacy.render(_statement, style='ent', minify=True)
    return render_template('statement.html', statement=_statement, ents=_spacy_html, persons=_persons)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
