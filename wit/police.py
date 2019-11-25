#!/usr/bin/env python

import spacy

from flask import render_template, request, url_for
from spacy import displacy
from spacy.tokens import Doc
from peewee import JOIN

from wit import app, db
from wit.models import Case, Code, Witness, Entity, Statement, EntityStatement

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
    return render_template('case.html', case=case, crumbs=crumbs, selected='graph')

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
    return render_template('witnesses.html', case=case, witnesses=witnesses, crumbs=crumbs, selected='witnesses')

@app.route('/cases/<uuid:case_id>/statements', methods=['GET'])
def statements(case_id):
    case = Case.get_by_id(case_id)
    statements = (Statement
                  .select()
                  .join(Code)
                  .join(Witness)
                  .where(Statement.case == case))
    crumbs = [
            ('cases', url_for('cases')),
            (case.name, url_for('case', id=case_id)),
            ('statements', url_for('statements', case_id=case_id)),
            ]
    return render_template('statements.html', case=case, statements=statements, crumbs=crumbs, selected='statements')

@app.route('/cases/<uuid:case_id>/entities', methods=['GET'])
def entities(case_id):
    case = Case.get_by_id(case_id)
    entities = (Entity.select().join(EntityStatement).join(Statement).where(Statement.case_id == case_id).group_by(Entity))
    crumbs = [
            ('cases', url_for('cases')),
            (case.name, url_for('case', id=case_id)),
            ('entities', url_for('entities', case_id=case_id)),
            ]
    return render_template('entities.html', case=case, entities=entities, crumbs=crumbs, selected='entities')

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
        entity_id = f'entity--{pair.entity.id}'
        statement_id = f'statement--{pair.statement.id}'
        links.append({ 'source': statement_id, 'target': entity_id, 'label': '' })
        if statement_id not in ids:
            nodes.append({ 'id': statement_id, 'type': 'statement', 'label': pair.statement.id, 'size': 10, 'href': url_for('statement', case_id=id, id=pair.statement.id) })
            ids.add(statement_id)
        if entity_id not in ids:
            nodes.append({ 'id': entity_id, 'type': 'entity', 'label': f'{pair.entity.label}: {pair.entity.text}', 'size': 5, 'href': url_for('entity', case_id=id, id=pair.entity.id) })
            ids.add(entity_id)
    return { 'links': links, 'nodes': nodes }

@app.route('/cases/<uuid:case_id>/statements/<uuid:id>')
def statement(case_id, id):
    case = Case.get_by_id(case_id)
    statement = Statement.get_by_id(id)
    doc = Doc(spacy.blank("en").vocab).from_bytes(statement.spacy_doc)
    spacy_html = displacy.render(doc, style='ent', minify=True)
    crumbs = [
            ('cases', url_for('cases')),
            (case.name, url_for('case', id=case_id)),
            ('statements', url_for('statements', case_id=case_id)),
            (f'statement ({statement.code.witness.name})', url_for('statement', case_id=case_id, id=id)),
            ]
    return render_template('statement.html', statement=statement, ents=spacy_html, crumbs=crumbs)

@app.route('/cases/<uuid:case_id>/entities/<uuid:id>')
def entity(case_id, id):
    case = Case.get_by_id(case_id)
    return render_template('entities.html')

@app.route('/cases/<uuid:case_id>/witnesses/<uuid:id>')
def witness(case_id, id):
    return 'lol'
