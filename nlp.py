import fileinput
import re
import sys

import spacy
from spacy import displacy
from spacy.pipeline import EntityRuler

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")
docs = []

# Process whole documents
for fn in sys.argv[1:]:
  print(fn)

  with open(fn) as f:
    text = f.read()
    doc = nlp(text)

    # Process registrations/postcodes
    expr = r'[A-Z][A-Z0-9 ]+'

    for match in re.finditer(expr, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        if span:
            print('MATCH: ', span.text)
            with doc.retokenize() as rtk:
                rtk.merge(span, {'ENT_TYPE': 'REG'})

    # Analyze syntax
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    for token in doc:
        print(token.pos_, token.lemma_)

    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)

    docs.append(doc)

#displacy.serve(docs, style='ent')
