import pytest
from datamapper.app import app
from datamapper.app.views import mock_ajax


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