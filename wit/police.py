#!/usr/bin/env python

from flask import render_template, request, url_for
from spacy import displacy

from wit import app, db
from wit.models import Case, Witness

@app.route('/cases')
def cases():
    with db:
        cases = Case.select().where(Case.closed.is_null())
    return render_template('cases.html', cases=cases)

@app.route('/cases', methods=['POST'])
def create_case():
    return 'created a case m8'

@app.route('/cases/<uuid:id>', methods=['GET'])
def case(id):
    case = Case.get_by_id(id)
    crumbs = [
            ('cases', url_for('cases')),
            (case.name, url_for('case', id=id)),
            ]
    return render_template('case.html', case=case, crumbs=crumbs)

@app.route('/new_case')
def new_case():
    return 'new case'

@app.route('/cases/<uuid:case_id>/witnesses', methods=['GET'])
def witnesses(case_id):
    case = Case.get_by_id(case_id)
    witnesses = case.witnesses
    crumbs = [
            ('cases', url_for('cases')),
            (case.name, url_for('case', id=case_id)),
            ('witnesses', url_for('witnesses', case_id=case_id)),
            ]
    return render_template('witnesses.html', case=case, witnesses=witnesses, crumbs=crumbs)
