#!/usr/bin/env python

from flask import render_template, request
from jinja2 import Environment, FileSystemLoader, select_autoescape
from spacy import displacy

from wit import app
from wit.nlp import process_text

@app.route('/')
def auth():
    return render_template('witness_auth.html', next='/give-statement')

@app.route('/give-statement')
def give_statement():
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
        _added = []

        for ent in _statement.ents:
            if ent.text not in _added:
                if ent.label_ == 'PRODUCT':
                    _hints.append({ 'ent': ent, 'prompt': 'more detail' })
                    _added.append(ent.text)
                elif ent.label_ == 'PLACE':
                    _hints.append({ 'ent': ent, 'prompt': 'an address' })
                    _added.append(ent.text)

        return render_template('witness_statement.html', statement_text=_spacy_html, hints=_hints, next='/give-statement/advokate')
    return render_template('witness_statement.html', next='/give-statement/advokate')

@app.route('/give-statement/advokate', methods=['GET','POST'])
def advokate():
    return render_template('witness_advokate.html', next='/give-statement/summary')

@app.route('/give-statement/summary')
def summary():
    return render_template('witness_summary.html', next='/give-statement/done')

@app.route('/give-statement/done')
def done():
    return render_template('witness_done.html')
