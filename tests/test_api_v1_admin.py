from app import db

def test_non_admin_gets_403_on_admin_jokes(regular_client):
    """
    GIVEN a logged-in user with role 'user'
    WHEN they send GET /api/v1/admin/jokes
    THEN the response should be 403 FORBIDDEN

    Level: ERROR CASE
    """
    response = regular_client.get('/api/v1/admin/jokes')
    assert response.status_code == 403
    assert response.get_json()['error']['code'] == 'FORBIDDEN'


def test_non_admin_gets_403_on_delete(regular_client, sample_jokes):
    """
    GIVEN a logged-in user with role 'user'
    WHEN they send DELETE /api/v1/admin/jokes/<id>
    THEN the response should be 403 FORBIDDEN

    Level: ERROR CASE
    """
    response = regular_client.delete(f'/api/v1/admin/jokes/{sample_jokes[0].id}')
    assert response.status_code == 403


def test_unauthenticated_gets_401_on_admin_route(client):
    """
    GIVEN an unauthenticated client (no session)
    WHEN they send GET /api/v1/admin/jokes
    THEN the response should be 401 UNAUTHORIZED

    Level: ERROR CASE
    """
    response = client.get('/api/v1/admin/jokes')
    assert response.status_code == 401


def test_admin_get_all_jokes(admin_client, sample_jokes):
    """
    GIVEN an admin user and 3 jokes (1 flagged, 2 unflagged)
    WHEN they send GET /api/v1/admin/jokes
    THEN the response should be 200 with all 3 jokes

    Level: HAPPY PATH
    """
    response = admin_client.get('/api/v1/admin/jokes')
    assert response.status_code == 200
    jokes = response.get_json()['data']['jokes']
    assert len(jokes) == 3


def test_admin_get_flagged_only(admin_client, sample_jokes):
    """
    GIVEN an admin user and 3 jokes (1 flagged)
    WHEN they send GET /api/v1/admin/jokes?flagged=true
    THEN the response should return only the flagged joke

    Level: EDGE CASE
    """
    response = admin_client.get('/api/v1/admin/jokes?flagged=true')
    assert response.status_code == 200
    jokes = response.get_json()['data']['jokes']
    assert len(jokes) == 1
    assert jokes[0]['flagged'] is True


def test_admin_delete_joke(admin_client, sample_jokes):
    """
    GIVEN an admin user and a joke with a known id
    WHEN they send DELETE /api/v1/admin/jokes/<id>
    THEN the response should be 204 and the joke should be gone

    Level: HAPPY PATH
    """
    joke_id = sample_jokes[0].id
    response = admin_client.delete(f'/api/v1/admin/jokes/{joke_id}')
    assert response.status_code == 204
    # Confirm it's gone
    follow_up = admin_client.get('/api/v1/admin/jokes')
    ids = [j['id'] for j in follow_up.get_json()['data']['jokes']]
    assert joke_id not in ids


def test_admin_flag_joke_toggles(admin_client, sample_jokes):
    """
    GIVEN an admin user and an unflagged joke
    WHEN they PATCH /api/v1/admin/jokes/<id>/flag with {"flagged": true}
    THEN the joke should be flagged; patching again with false unflags it
    Level: HAPPY PATH
    """
    joke_id = sample_jokes[0].id  # unflagged
    # Flag it
    res1 = admin_client.patch(f'/api/v1/admin/jokes/{joke_id}/flag',
                              json={'flagged': True})
    assert res1.status_code == 200
    assert res1.get_json()['data']['joke']['flagged'] is True
    # Unflag it
    res2 = admin_client.patch(f'/api/v1/admin/jokes/{joke_id}/flag',
                              json={'flagged': False})
    assert res2.status_code == 200
    assert res2.get_json()['data']['joke']['flagged'] is False


def test_regular_user_does_not_see_flagged_jokes(authenticated_client, sample_jokes):
    """
    GIVEN an authenticated regular user and 3 jokes (1 flagged)
    WHEN they send GET /api/v1/jokes
    THEN the response should contain only the 2 unflagged jokes

    Level: EDGE CASE
    """
    regular_client.post('/api/v1/jokes', json={"text": "A qualifying joke submission."})
    response = regular_client.get('/api/v1/jokes')
    assert response.status_code == 200
    data = response.get_json()
    jokes = data['data']['jokes']
    assert len(jokes) == 3 
    assert all(j.get('flagged') is False for j in jokes)
