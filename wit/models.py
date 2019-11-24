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
class User(BaseModel):
    username = CharField()
    password = CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = False

    def get_id(self):
        return self.id

class Case(BaseModel):
    opened = DateTimeField(default=datetime.now)
    closed = DateTimeField(null=True)
    name = CharField(index=True)

class Witness(BaseModel):
    case = ForeignKeyField(Case, backref='witnesses')
    name = CharField(index=True)
    birthdate = DateField(null=True)
    address = TextField(null=True)
    postcode = CharField(null=True)
    mobile = CharField(null=True)
    email = CharField(null=True)

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
