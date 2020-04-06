import mongoengine as me
import datetime

me.connect('SHOP_DB')


class Customer(me.Document):
    user_id = me.IntField(unique=True)
    username = me.StringField(min_length=1, max_length=256)
    phone_number = me.StringField(min_length=12)
    address = me.StringField()
    first_name = me.StringField(min_length=1, max_length=256)
    surname = me.StringField(min_length=1, max_length=256)
    age = me.IntField(min_value=12, max_value=99)


class Characteristics(me.EmbeddedDocument):
    height = me.DecimalField()
    width = me.DecimalField()
    weight = me.DecimalField()


class Category(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    slug = me.StringField(min_length=2, max_length=512, unique=True, required=True)
    description = me.StringField(min_length=2, max_length=2048)
    #Self or Category - reference to current collection
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self')


class Product(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    slug = me.StringField(min_length=2, max_length=512, unique=True, required=True)
    description = me.StringField(min_length=2, max_length=2048)
    characteristics = me.EmbeddedDocumentField(Characteristics)
    price = me.DecimalField(min_value=0, force_string=True, required=True)
    category = me.ReferenceField(Category)


class News(me.Document):
    title = me.StringField(min_length=2, max_length=512)
    body = me.StringField(min_length=10, max_length=4096)
    pub_date = me.DateTimeField(default=datetime.datetime.now)


class Texts(me.Document):
    choices = (
        ('Greeting', 'Greeting'),
        ('Buy', 'Buy')
    )
    text = me.StringField(choices=choices)
