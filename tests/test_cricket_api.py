import pytest
from unittest.mock import patch, Mock
from utils.cricket_api import get_current_matches, format_scores, CricketAPIError

def test_scores():
    assert format_scores({'score': [{'inning': 'India', 'r': 170, 'w': 4, 'o': 18.2}]}) == 'India: 170/4 (18.2 overs)'
    assert format_scores({}) == 'Score not available'

def test_api_success(monkeypatch):
    monkeypatch.setenv('CRICKET_API_KEY', 'fake-test-key')
    fake = Mock()
    fake.json.return_value = {'status': 'success', 'data': [{'name': 'Test Match'}]}
    with patch('utils.cricket_api.requests.get', return_value=fake) as request:
        assert get_current_matches() == [{'name': 'Test Match'}]
        assert request.call_args.kwargs['timeout'] == 12

def test_missing_key(monkeypatch):
    monkeypatch.delenv('CRICKET_API_KEY', raising=False)
    with patch('utils.cricket_api.load_dotenv'):
        with pytest.raises(CricketAPIError):
            get_current_matches()

def test_api_failure(monkeypatch):
    monkeypatch.setenv('CRICKET_API_KEY', 'fake-test-key')
    fake = Mock()
    fake.json.return_value = {'status': 'failure', 'reason': 'invalid key'}
    with patch('utils.cricket_api.requests.get', return_value=fake):
        with pytest.raises(CricketAPIError):
            get_current_matches()
