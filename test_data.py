import os
from datetime import datetime
from glob import glob
from wit import app, db
from wit.nlp import process_text
from wit.models import Case, Witness, Code, Statement, Entity, EntityStatement

def create_statement(case, witness, text, supervised=False):
    doc = process_text(text)
    code = Code.create(witness=witness, used=datetime.now())
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
        text1 = '''
        I saw a murder in Overton Park.
        '''
        create_statement(case, witness1, text1, supervised=True)

        witness2 = Witness.create(case=case, name='Becky Parks', mobile='01234788961', email='becky.parks@example.com')
        text2 =  '''
        There was an attack in Overton Park by the swings.
        I think I recognised Jim Burns from down the road.
        '''
        create_statement(case, witness2, text2, supervised=True)

        clue = Case.create(name='Clue Case')

        for path in glob('statements/statement-*.txt'):
            witness_name = path.replace('statements/statement-', '').replace('.txt', '').replace('-', ' ').title()
            cwit = Witness.create(case=clue, name=witness_name)
            create_statement(clue, cwit, open(path).read(), supervised=True)
