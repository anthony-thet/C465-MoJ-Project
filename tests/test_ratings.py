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
        # TODO: Implement
        pass

    # --- EDGE CASES ---

    # TODO: Add at least one edge case test
    #   Suggestions from L7 Slide 15:
    #   - Boundary values (scores of 1 and 5)
    #   - PUT update changes values (idempotent update)

    # --- ERROR CASES ---

    # TODO: Add at least two error case tests
    #   Suggestions from L7 Slide 15:
    #   - Duplicate POST → 409
    #   - Score out of range → 400
    #   - Unauthenticated → 401
    #   - Nonexistent joke → 404
