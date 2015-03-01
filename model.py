__author__ = 'wuwy'
from peewee import *
from zhihuSpider import db


class User(db.BaseModel):
    def __init__(self):
        self.user_name    = CharField()
        self.flower_count = IntegerField()
        self.image_url    = CharField()
        self.agree        = IntegerField()
        self.thanks       = IntegerField()
        self.answer_count = IntegerField()
        self.location     = CharField()
        self.fav          = IntegerField()
        self.share        = CharField()
        self.company      = CharField()
        self.position     = CharField()
        self.school       = CharField()
        self.url          = CharField()
        self.img_url      = CharField()
        self.img_file     = CharField()
        self.major        = CharField()

    class Meta:
        database = db