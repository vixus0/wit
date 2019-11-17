from datetime import datetime
from uuid import uuid4
from peewee import (
        Model,
        BlobField,
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

class Witness(BaseModel):
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
    witness = ForeignKeyField(Witness, backref='statements')
    submitted = DateTimeField(default=datetime.now, index=True)
    text = TextField()
    spacy_doc = BlobField()
