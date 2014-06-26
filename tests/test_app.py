import pytest
from datamapper.app import app as _app
from datamapper.app import db as _db
from datamapper.app.views import mock_ajax
from datamapper.app.models import State, Data, DataSet


TEST_DATABASE_URI = 'postgresql://ian:heatmapper@localhost/test_heatmapper'


@pytest.yield_fixture(scope='function')
def req_context():
    """run tests within a test request context so that 'g' is present"""
    with _app.test_request_context('/mock-ajax'):
        yield

@pytest.fixture(scope='session')
def seed_data(session):
    #import pdb; pdb.set_trace()
    data = [
                State('New York', 'NY', 42.1497, -74.9384),
                State('New Jersey', 'NJ', 42.1497, -74.9384),
                State('New Hampshire', 'NH', 42.1497, -74.9384),
                State('Florida', 'FL', 42.1497, -74.9384),
                State('New Mexcio', 'NM', 42.1497, -74.9384),
                State('Ohio', 'OH', 42.1497, -74.9384),
                DataSet('Unemployment'),
                DataSet('Housing Starts'),
                DataSet('Real Gdp'),
                DataSet('Assets Commercial Banks')
            ]
    for d in data:
        _db.session.add(d)
        _db.session.commit()

    data_points = [
                Data('NY', 'Unemployment', .12, '1/1/14'),
                Data('NY', 'Unemployment', .11, '6/1/13'),
                Data('NY', 'Unemployment', .10, '1/1/13'),
                Data('NY', 'Unemployment', .13, '6/1/12'),
                Data('NY', 'Unemployment', .08, '1/1/12'),
                Data('NY', 'Unemployment', .05, '6/1/11'),
                Data('NY', 'Unemployment', .10, '1/1/11'),
                Data('NY', 'Unemployment', .12, '6/1/10'),
                Data('NY', 'Unemployment', .18, '1/1/10'),
                Data('NY', 'Unemployment', .13, '6/1/09'),
                Data('NY', 'Unemployment', .05, '1/1/09'),
                Data('NY', 'Real Gdp', .05, '1/1/09'),
                Data('NY', 'Housing Starts', 374, '6/1/14'),
                Data('NY', 'Assets Commercial Banks', .12, '6/1/14'),
                Data('NJ', 'Unemployment', .12, '6/1/14'),
                Data('NJ', 'Real Gdp', 900000, '6/1/14'),
                Data('NJ', 'Housing Starts', 374, '6/1/14'),
                Data('NJ', 'Assets Commercial Banks', .12, '6/1/14'),
                Data('NH', 'Unemployment', .12, '6/1/14'),
                Data('NH', 'Real Gdp', 800000, '6/1/14'),
                Data('NH', 'Housing Starts', 374, '6/1/14'),
                Data('NH', 'Assets Commercial Banks', .12, '6/1/14'),
                Data('FL', 'Unemployment', .12, '6/1/14'),
                Data('FL', 'Real Gdp', 500000, '6/1/14'),
                Data('FL', 'Housing Starts', 374, '6/1/14'),
                Data('FL', 'Assets Commercial Banks', .12, '6/1/14'),
                Data('NM', 'Unemployment', .12, '6/1/14'),
                Data('NM', 'Real Gdp', 600000, '6/1/14'),
                Data('NM', 'Housing Starts', 374, '6/1/14'),
                Data('NM', 'Assets Commercial Banks', .12, '6/1/14'),
                Data('OH', 'Unemployment', .12, '6/1/14'),
                Data('OH', 'Real Gdp', 800000, '6/1/14'),
                Data('OH', 'Housing Starts', 374, '6/1/14'),
                Data('OH', 'Assets Commercial Banks', .12, '6/1/14'),
            ]
    for dp in data_points:
        _db.session.add(dp)
        _db.session.commit()


@pytest.fixture(scope='session')
def app(request):
    _app.config['TESTING'] = True,
    _app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    # This line breaks the tests but was included in the tutorial,
    # may be important later.
    # options = dict(bind=connection, binds={})
    session = db.create_scoped_session()

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

def test_mock_ajax(req_context):
    mock = mock_ajax()
    assert mock

def test_state_model():
    ny = State('Arizona', 'AZ', 42.1497, -74.9384)
    assert ny.short_name == 'AZ'

def test_db(session):
    ct = State('Connecticut', 'CT', 42.1497, -74.9384)
    _db.session.add(ct)
    _db.session.commit()
    assert ct.id > 0

def test_data_set(session):
    data_set = DataSet('Unemployment')
    _db.session.add(data_set)
    _db.session.commit()
    assert data_set.id > 0

def test_data_model(session, seed_data):
    data = Data('NY', 'Unemployment', .12, '6/22/14')
    expected_state = State.query.filter(State.short_name == 'NY').one()
    assert data.state_id == expected_state.id

def test_date_range_query(session):
    data = Data.query.filter(Data.date.between('6/1/09', '6/1/12')).all()
    assert len(data) == 7

def test_data_set_query(session):
    data = Data.query.filter(Data.data_set == 1).all()
    print([dp.date for dp in data])
    assert 0