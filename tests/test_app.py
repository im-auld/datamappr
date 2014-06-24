import pytest
from datamapper.app import app
from datamapper.app.views import mock_ajax
from datamapper.app.models import State, Data


@pytest.fixture(scope='session')
def test_app():
    datamapper.app.config['TESTING'] = True

@pytest.yield_fixture(scope='session')
def req_context():
    with app.test_request_context('/mock_ajax'):
        yield

def test_mock_ajax(req_context):
    mock = mock_ajax()
    assert mock

def test_state_model():
    ny = State('New York', 'NY', 42.1497, -74.9384)
    assert ny.short_name == 'NY'