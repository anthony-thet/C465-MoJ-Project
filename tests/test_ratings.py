import pytest


class TestRatings:
    """Rating endpoint tests — organized by the three-level taxonomy from L7."""

    # --- HAPPY PATH ---

    def test_create_rating(self, client, auth_headers, sample_joke):
        """
        GIVEN an authenticated user and an existing joke
        WHEN they POST a valid rating to /jokes/<id>/ratings
        THEN the response should be 201 with the rating data

        Level: HAPPY PATH
        """
        payload = {
            "funniness": 4,
            "appropriateness": 5,
            "originality": 3
        }

        response = client.post(
            f"/jokes/{sample_joke.id}/ratings",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 201

        data = response.get_json()
        assert data["funniness"] == 4
        assert data["appropriateness"] == 5
        assert data["originality"] == 3

    # --- EDGE CASES ---

    def test_create_rating_boundary_scores(self, client, auth_headers, sample_joke):
        """
        GIVEN an authenticated user and an existing joke
        WHEN they POST a rating using boundary scores 1 and 5
        THEN the response should be 201

        Level: EDGE CASE
        """
        payload = {
            "funniness": 1,
            "appropriateness": 5,
            "originality": 1
        }

        response = client.post(
            f"/jokes/{sample_joke.id}/ratings",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["funniness"] == 1
        assert data["appropriateness"] == 5
        assert data["originality"] == 1

    # --- ERROR CASES ---

    def test_duplicate_rating_returns_409(self, client, auth_headers, sample_joke):
        """
        GIVEN an authenticated user who already rated a joke
        WHEN they POST a second rating to the same joke
        THEN the response should be 409

        Level: ERROR CASE
        """
        payload = {
            "funniness": 4,
            "appropriateness": 4,
            "originality": 4
        }

        first = client.post(
            f"/jokes/{sample_joke.id}/ratings",
            json=payload,
            headers=auth_headers
        )
        assert first.status_code == 201

        second = client.post(
            f"/jokes/{sample_joke.id}/ratings",
            json=payload,
            headers=auth_headers
        )

        assert second.status_code == 409
        data = second.get_json()
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]

    def test_out_of_range_score_returns_400(self, client, auth_headers, sample_joke):
        """
        GIVEN an authenticated user and an existing joke
        WHEN they POST a rating with a score outside 1-5
        THEN the response should be 400

        Level: ERROR CASE
        """
        payload = {
            "funniness": 0,
            "appropriateness": 5,
            "originality": 3
        }

        response = client.post(
            f"/jokes/{sample_joke.id}/ratings",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "code" in data["error"]
