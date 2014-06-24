import pytest
from app.views import mock_ajax

def test_mock_ajax():
    mock = mock_ajax()
    assert mock