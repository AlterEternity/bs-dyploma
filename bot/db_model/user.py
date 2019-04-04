from mongoengine import *


class User(Document):
    """
    User document in db
    Fields: user_id, username, first_name, last_name, state, language
    """
    user_id = IntField(required=True, unique=True)
    username = StringField

    first_name = StringField()
    last_name = StringField()

    state = IntField()
    user_lang = StringField(default='eng')
