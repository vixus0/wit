#!/usr/bin/env python

from flask import render_template, request
from spacy import displacy

generate_json()

env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape = select_autoescape(['html', 'css'])
        )

app = Flask(__name__)

@app.route('/cases', methods=['GET', 'POST'], defaults={'id': None})
@app.route('/cases/<uuid:id>', methods=['GET'])
def index(id):
    return render_template('cases.html', persons=_persons, statements=_statements)

@app.route('/witnesses', methods=['GET', 'POST'], defaults={'id': None})
@app.route('/witnesses/<uuid:id>', methods=['GET'])
def witnesses(id):
    if request.method == 'GET':
        if id:
            return f'id: {id}'
        else:
            return 'list it bra'
    elif request.method == 'POST':
        return 'post it brew'

@app.route('/statements', methods=['GET', 'POST'], defaults={'id': None})
@app.route('/statements/<uuid:id>', methods=['GET'])
def statements(id):
    if request.method == 'GET':
        if id:
            return f'id: {id}'
        else:
            return 'list it bra'
    elif request.method == 'POST':
        return 'post it brew'

@app.route('/cases/<uuid:id>/codes', method=['GET', 'POST'])
def codes():
    '''List codes or generate a new one'''
    if request.method == 'GET':
        return 'list codes'
    elif request.method == 'POST':
        return 'generate new code'

@app.route('/phrase', methods=['POST'])
def phrase():
    '''Check validity of a passphrase'''
    pass
