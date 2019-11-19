import fileinput
import sys
import spacy

from wit import app

nlp = spacy.load(app.config['SPACY_MODEL'])

def process(fn):
  with open(fn) as f:
    text = f.read()
    return process_text(text)

def process_text(text):
    return nlp(text)

if __name__ == '__main__':
    for fn in sys.argv[1:]:
        doc = process_text(fn)
        for ent in doc.ents:
            print(ent.text, ent.label_)
