import fileinput
import sys

import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler

nlp = spacy.load('en_core_web_sm')
#nlp = English()

patterns = [{"label": "PERSON", "pattern": "Anshul Sirur"},
            {"label": "VEHICLE", "pattern": "car"},
            {"label": "PLACE", "pattern": [{"LOWER": "bermondsey"}, {"LOWER": "street"}]},
            {"label": "TIME", "pattern": [{"SHAPE": "dd:dd"}]},
            {"label": "PERSON", "pattern": "shop attendant"},
            {"label": "PERSON", "pattern": "security guard"},
            {"label": "PERSON", "pattern": "injured"},
            {"label": "PLACE", "pattern": "the shop"},
            ]

ruler = EntityRuler(nlp, overwrite_ents=True)
ruler.add_patterns(patterns)

nlp.add_pipe(ruler)

def process(fn):
  with open(fn) as f:
    text = f.read()
    return nlp(text)

def process_text(text):
    return nlp(text)

if __name__ == '__main__':
    for fn in sys.argv[1:]:
        doc = process(fn)
        for ent in doc.ents:
            print(ent.text, ent.label_)

