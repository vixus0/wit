from datetime import datetime
from uuid import uuid4
from peewee import (
        Model,
        BlobField,
        BooleanField,
        CharField,
        DateField,
        DateTimeField,
        ForeignKeyField,
        TextField,
        UUIDField
        )
from passphrase import Passphrase

from wit import db

def generate_phrase():
    pp = Passphrase('wordlist-short')
    pp.amount_n = 0
    pp.amount_w = 6
    return ' '.join(pp.generate())

class BaseModel(Model):
    class Meta:
        database = db
    id = UUIDField(primary_key=True, default=uuid4)

#
# Case -> Witness -> Code -> Statement
#
class User(Model):
    username = CharField()
    password = CharField()

class Case(Model):
    opened = DateTimeField(default=datetime.now)
    closed = DateTimeField(null=True)
    name = CharField(index=True)
    created_by = ForeignKeyField(User, backref='cases')

class Witness(BaseModel):
    case = ForeignKeyField(Case, backref='witnesses')
    name = CharField(index=True)
    birthdate = DateField()
    address = TextField()
    mobile = CharField()
    email = CharField()

class Code(BaseModel):
    witness = ForeignKeyField(Witness, backref='codes')
    phrase = CharField(index=True, default=generate_phrase)
    generated = DateTimeField(default=datetime.now)
    used = DateTimeField(null=True)

class Statement(BaseModel):
    code = ForeignKeyField(Code, backref='statements')
    submitted = DateTimeField(default=datetime.now, index=True)
    text = TextField()
    spacy_doc = BlobField()
    supervised = BooleanField()
