import fileinput
import sys

import spacy

nlp = spacy.load("en_core_web_lg")

def process(fn):
  with open(fn) as f:
    text = f.read()
    return nlp(text)

if __name__ == '__main__':
    for fn in sys.argv[1:]:
        doc = process(fn)
        for ent in doc.ents:
            print(ent.text, ent.label_)
