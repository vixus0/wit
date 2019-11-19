import os

DATABASE = os.getenv('SQLITE_DB', default=':memory:')
SPACY_MODEL = "en_core_web_sm"
