from peewee import Model, MySQLDatabase
db = MySQLDatabase("zhihu_data.db", host='192.168.14.31', user='zhihu', passwd='root')


class BaseModel(Model):
    class Meta:
        database = db