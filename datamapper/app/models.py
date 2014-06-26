from datamapper.app import db


class State(db.Model):
    __tablename__ = 'State'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    short_name = db.Column(db.String(2), nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, name, short_name, latitude, longitude):
        self.name = name.title()
        self.short_name = short_name.upper()
        self.latitude = latitude
        self.longitude = longitude


class Data(db.Model):
    __tablename__ = 'Data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_id = db.Column(db.Integer, db.ForeignKey('State.id'))
    data_set = db.Column(db.Integer, db.ForeignKey('DataSet.id'))
    raw_data = db.Column(db.Float, nullable=False)
    normalized_data = db.Column(db.Float)
    date = db.Column(db.Date, nullable=False)


    def __init__(self, state, data_set, raw_data, date,normalized_data = None):
        db_state = State.query.filter(State.short_name == state.upper()).first()
        db_data_set = DataSet.query.filter(DataSet.name == data_set.title()).first()
        self.state_id = db_state.id
        self.data_set = db_data_set.id
        self.raw_data = raw_data
        self.date = date
        self.normalized_data = normalized_data


class DataSet(db.Model):
    __tablename__ = 'DataSet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name.title()