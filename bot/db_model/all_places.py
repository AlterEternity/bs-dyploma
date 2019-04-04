from mongoengine import *

occupancy = ('Available', 'Not Available')


class Places(Document):
    """
    Document for storing info about all places
    Fields: sector, raw, place, availability, price
    """
    sector = StringField()
    raw = StringField()
    place = StringField(null=False)
    availability = StringField(choices=occupancy)
    price = FloatField()
