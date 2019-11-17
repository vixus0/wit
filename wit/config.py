import os

DATABASE = os.getenv('SQLITE_DB', default=':memory:')
