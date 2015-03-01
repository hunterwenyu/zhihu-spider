from peewee import Model,MySQLDatabase

db = MySQLDatabase("zhihu_data.db")


class BaseModel(Model):
    class Meta:
        database = db