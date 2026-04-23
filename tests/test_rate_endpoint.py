from unittest.mock import patch, MagicMock
import requests

def test_rate_joke_stores_ai_rating(authenticated_client, sample_joke):
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "7"}
    mock_response.raise_for_status.return_value = None
    with patch('requests.post', return_value=mock_response):
        resp = authenticated_client.post(f'/api/v1/jokes/{sample_joke.id}/rate')
    assert resp.status_code == 200
    assert resp.get_json()['data']['ai_rating'] == 7

def test_rate_joke_handles_ollama_unavailable(authenticated_client, sample_joke):
    with patch('requests.post', side_effect=requests.exceptions.ConnectionError()):
        resp = authenticated_client.post(f'/api/v1/jokes/{sample_joke.id}/rate')
    assert resp.status_code == 503
    assert resp.get_json()['error']['code'] == 'OLLAMA_UNAVAILABLE'
