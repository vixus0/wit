import os

DATABASE = os.getenv('SQLITE_DB', default='test.db')
SECRET_KEY = os.getenv('SECRET_KEY', default=os.urandom(16))
SPACY_MODEL = "en_core_web_sm"
FLASK_RUN_PORT = os.getenv('PORT', default=5000)
