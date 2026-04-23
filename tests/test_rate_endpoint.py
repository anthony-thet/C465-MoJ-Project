import pytest
import requests
from unittest.mock import patch, MagicMock
from app.models import Joke, db as _db
from app.models import parse_rating 


def test_rate_joke_stores_ai_rating(authenticated_client, sample_joke):
    """
    GIVEN a logged-in user and an existing joke
    WHEN they POST to /api/v1/jokes/<id>/rate and the LLM returns a rating
    THEN the response is 200 and the joke's ai_rating is updated in the DB
    
    Level: HAPPY PATH
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "7"}
    mock_response.raise_for_status.return_value = None
    
    with patch('requests.post', return_value=mock_response):
        resp = authenticated_client.post(f'/api/v1/jokes/{sample_joke.id}/rate')
    
    assert resp.status_code == 200
    assert resp.get_json()['data']['ai_rating'] == 7


def test_rate_joke_handles_ollama_unavailable(authenticated_client, sample_joke):
    """
    GIVEN a logged-in user
    WHEN the LLM service is down (ConnectionError)
    THEN the response is 503 with OLLAMA_UNAVAILABLE code
    
    Level: ERROR CASE
    """
    with patch('requests.post', side_effect=requests.exceptions.ConnectionError()):
        resp = authenticated_client.post(f'/api/v1/jokes/{sample_joke.id}/rate')
    
    assert resp.status_code == 503
    assert resp.get_json()['error']['code'] == 'OLLAMA_UNAVAILABLE'


## --- Phase 2: Stub Implementations ---

def test_rate_joke_unauthenticated(client, sample_joke):
    """
    Stub A — Unauthenticated request
    GIVEN an unauthenticated client (no session)
    WHEN they POST to /api/v1/jokes/<id>/rate
    THEN the response is 401 UNAUTHORIZED
    
    Level: ERROR CASE
    """
    resp = client.post(f'/api/v1/jokes/{sample_joke.id}/rate')
    assert resp.status_code == 401


def test_parse_rating_extracts_from_prose():
    """
    Stub B — parse_rating: prose response
    GIVEN the string "I'd give it a 7 out of 10"
    WHEN parse_rating() is called
    THEN it returns the integer 7
    
    Level: EDGE CASE
    """
    text = "I'd give it a 7 out of 10"
    result = parse_rating(text)
    assert result == 7
    assert isinstance(result, int)


def test_parse_rating_returns_none_when_no_number():
    """
    Stub C — parse_rating: no number found
    GIVEN the string "This joke is inappropriate."
    WHEN parse_rating() is called
    THEN it returns None
    
    Level: ERROR CASE
    """
    text = "This joke is inappropriate."
    result = parse_rating(text)
    assert result is None


def test_ai_rating_appears_in_joke_list(authenticated_client, sample_joke, app):
    """
    Stub D — ai_rating appears in joke list
    GIVEN a joke that has been rated (ai_rating = 9)
    WHEN an authenticated user GETs /api/v1/jokes
    THEN the response envelope includes ai_rating as an integer for that joke
    
    Level: HAPPY PATH
    """
    with app.app_context():
        joke_in_db = Joke.query.get(sample_joke.id)
        joke_in_db.ai_rating = 9
        _db.session.commit()

    response = authenticated_client.get('/api/v1/jokes')
    assert response.status_code == 200
    
    jokes = response.get_json()['data']['jokes']
    target = next((j for j in jokes if j['id'] == sample_joke.id), None)
    
    assert target is not None
    assert target['ai_rating'] == 9
