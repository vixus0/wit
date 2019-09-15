#!/usr/bin/env python

from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader, select_autoescape
from spacy import displacy

from dirty_nlp import process_text

env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape = select_autoescape(['html', 'css'])
        )

app = Flask(__name__)

@app.route('/')
def auth():
    return render_template('witness_auth.html', next='/give-statement')

@app.route('/give-statement')
def statement():
    return render_template('witness_start.html', next='/give-statement/personal-info')

@app.route('/give-statement/personal-info')
def basic_info():
    return render_template('witness_basic_info.html', next='/give-statement/care')

@app.route('/give-statement/care')
def care():
    return render_template('witness_care.html', next='/give-statement/consent')

@app.route('/give-statement/consent')
def consent():
    return render_template('witness_consent.html', next='/give-statement/statement')

@app.route('/give-statement/statement', methods=['GET', 'POST'])
def nlp():
    if request.method == 'POST':
        _statement = process_text(request.form['statement'])
        _spacy_html = displacy.render(_statement, style='ent', minify=True)
        _hints = []

        for ent in _statement.ents:
            if ent.label_ == 'VEHICLE':
                _hints.append({ 'ent': ent, 'prompt': 'more detail' })
            elif ent.label_ == 'PLACE':
                _hints.append({ 'ent': ent, 'prompt': 'an address' })

        return render_template('witness_statement.html', statement_text=_spacy_html, hints=_hints)
    return render_template('witness_statement.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
