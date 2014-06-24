from datamapper.app import db


class State(db.Model):
    __tablename__ = 'State'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    short_name = db.Column(db.String(2), nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

class Data(db.Model):
    __tablename__ = 'Data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_id = db.Column(db.Integer, db.ForeignKey('State.id'))
    raw_data = db.Column(db.Float, nullable=False)
    normalized_data = db.Column(db.Float)
    date = db.Column(db.Date, nullable=False)