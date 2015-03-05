from peewee import Model,MySQLDatabase
import pymysql
db = MySQLDatabase("zhihu_data.db")


class BaseModel(Model):
    class Meta:
        database = db