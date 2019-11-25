#!/usr/bin/env python

from flask import render_template, request, url_for
from spacy import displacy

from wit import app, db
from wit.models import Case, Witness, Entity, Statement, EntityStatement

@app.errorhandler(Case.DoesNotExist)
def handle_missing_case(e):
    return render_template('no_case.html', crumbs=[('cases', url_for('cases'))]), 404

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

@app.route('/cases/<uuid:id>/graph')
def graph(id):
    # node: id, type, label, size
    # link: source, target, label
    query = (EntityStatement
            .select(EntityStatement, Entity, Statement)
            .join(Entity)
            .switch(EntityStatement)
            .join(Statement)
            .where(Statement.case == id))
    links = []
    nodes = []
    ids = set()
    for pair in query:
        links.append({ 'source': pair.statement.id, 'target': pair.entity.id, 'label': '' })
        if pair.statement.id not in ids:
            nodes.append({ 'id': pair.statement.id, 'type': 'statement', 'label': pair.statement.id, 'size': 10 })
            ids.add(pair.statement.id)
        if pair.entity.id not in ids:
            nodes.append({ 'id': pair.entity.id, 'type': 'entity', 'label': f'{pair.entity.label}: {pair.entity.text}', 'size': 5 })
            ids.add(pair.entity.id)
    return { 'links': links, 'nodes': nodes }
