import os
import pytest
from datamapper.app import app as _app
from datamapper.app import db as _db
from datamapper.app.views import mock_ajax
from datamapper.app.models import State, Data


TEST_DATABASE_URI = 'postgresql://ian:heatmapper@localhost/test_heatmapper'


@pytest.yield_fixture(scope='function')
def req_context():
    """run tests within a test request context so that 'g' is present"""
    with _app.test_request_context('/mock-ajax'):
        yield

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
    ny = State('New York', 'NY', 42.1497, -74.9384)
    assert ny.short_name == 'NY'

def test_db(session):
    ny = State('New York', 'NY', 42.1497, -74.9384)
    _db.session.add(ny)
    _db.session.commit()
    assert ny.id > 0

def test_data_model(session):
    data = Data('NY', .12, '6/22/14')
    print(State.query.filter(State.short_name == 'NY').first().id)
    assert data.state_id == 1