import json
import sys
import os

from glob import glob
from collections import namedtuple, defaultdict

from nlp import process

data_dir = 'clue/data'
statements_dir = 'statements'

person_data = {}
statement_data = {}

with open(os.path.join(data_dir, 'persons.json')) as f:
    for person in json.load(f)['items']:
        person_data[person['fullName'].lower().replace(' ', '-')] = person

persons_statements = defaultdict(list)
statements_persons = defaultdict(list)

for fn in glob(os.path.join(statements_dir, 'statement-*.txt')):
    statement_key = os.path.basename(fn).replace('.txt', '')
    doc = process(fn)
    doc.user_data['title'] = statement_key
    statement_data[statement_key] = doc

    person_ents = set([ent for ent in doc.ents if ent.label_ == 'PERSON'])

    for ent in person_ents:
        person_key = ent.text.lower().replace(' ', '-')
        person = person_data.get(person_key, None)

        if person:
            persons_statements[person_key].append(statement_key)
            statements_persons[statement_key].append(person_key)

person_data = { id:person for id, person in person_data.items() if id in persons_statements.keys() }
