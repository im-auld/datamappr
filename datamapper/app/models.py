from flask.ext.sqlalchemy import sqlalchemy


db = SqlAlchemy()

class State(db.Model):
    pass

class Data(db.Model):
    pass

class DataType(db.Model):
    pass