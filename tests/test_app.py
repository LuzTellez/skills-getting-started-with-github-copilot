"""
Integration tests for the High School Management System FastAPI application.

All tests use the Arrange-Act-Assert (AAA) pattern for clarity:
- Arrange: Set up test data and fixtures
- Act: Perform the action being tested
- Assert: Verify the results meet expectations
"""

import pytest
from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Tests for the root endpoint (GET /)."""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that the root endpoint redirects to the static index.html page.
        
        Arrange: TestClient ready
        Act: Make GET request to /
        Assert: Verify redirect response to /static/index.html
        """
        # Arrange
        # (client fixture already provides TestClient)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for the activities list endpoint (GET /activities)."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns the complete list of available activities.
        
        Arrange: TestClient ready
        Act: Make GET request to /activities
        Assert: Verify response contains expected activities with correct structure
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Swimming Club",
            "Art Studio",
            "Drama Club",
            "Debate Team",
            "Science Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert set(data.keys()) == set(expected_activities)

    def test_activity_has_required_fields(self, client):
        """
        Test that each activity in the list contains all required fields.
        
        Arrange: TestClient ready
        Act: Make GET request to /activities
        Assert: Verify each activity has description, schedule, max_participants, and participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name, activity_data in data.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)


class TestSignupEndpoint:
    """Tests for the signup endpoint (POST /activities/{activity_name}/signup)."""

    def test_signup_adds_student_to_activity(self, client, test_activity, test_email):
        """
        Test that a student can successfully sign up for an activity.
        
        Arrange: Test email and activity name
        Act: Make POST request to signup endpoint
        Assert: Verify student is added and success message returned
        """
        # Arrange
        # (fixtures provide test_activity and test_email)

        # Act
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert test_activity in data["message"]

    def test_signup_verification_student_added_to_participants(self, client, test_activity, test_email):
        """
        Test that a signed-up student appears in the activity's participant list.
        
        Arrange: Test email and activity name
        Act: Signup student, then fetch activities list
        Assert: Verify student email is in participants list for that activity
        """
        # Arrange
        # (fixtures provide test_activity and test_email)

        # Act
        # First sign up the student
        signup_response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        assert signup_response.status_code == 200

        # Then fetch the updated activities list
        activities_response = client.get("/activities")

        # Assert
        assert activities_response.status_code == 200
        activities = activities_response.json()
        participants = activities[test_activity]["participants"]
        assert test_email in participants

    def test_signup_nonexistent_activity_returns_404(self, client, invalid_activity, test_email):
        """
        Test that attempting to sign up for a non-existent activity returns 404.
        
        Arrange: Invalid activity name and test email
        Act: Make POST request with non-existent activity
        Assert: Verify 404 status and appropriate error message
        """
        # Arrange
        # (fixtures provide invalid_activity and test_email)

        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_student_returns_400(self, client, test_activity):
        """
        Test that a student cannot sign up twice for the same activity.
        
        Arrange: Get existing participant from activity, prepare to sign them up again
        Act: Make POST request with email already in participants
        Assert: Verify 400 status and duplicate signup error message
        """
        # Arrange
        # Get an existing participant from the activity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        existing_email = activities[test_activity]["participants"][0]

        # Act
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]


class TestUnregisterEndpoint:
    """Tests for the unregister endpoint (DELETE /activities/{activity_name}/unregister)."""

    def test_unregister_removes_student_from_activity(self, client, test_activity, test_email):
        """
        Test that a student can successfully unregister from an activity.
        
        Arrange: Sign up student first, then prepare unregister request
        Act: Make DELETE request to unregister endpoint
        Assert: Verify success message and student is removed from participants
        """
        # Arrange
        # First sign up the student
        signup_response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        assert signup_response.status_code == 200

        # Act
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert test_activity in data["message"]

    def test_unregister_verification_student_removed_from_participants(self, client, test_activity, test_email):
        """
        Test that an unregistered student no longer appears in the activity's participant list.
        
        Arrange: Sign up student, then unregister, then fetch activities
        Act: Verify student is not in participants list
        Assert: Confirm removal was successful
        """
        # Arrange
        # Sign up the student
        client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )

        # Act
        # Unregister the student
        unregister_response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        assert unregister_response.status_code == 200

        # Then fetch the updated activities list
        activities_response = client.get("/activities")

        # Assert
        assert activities_response.status_code == 200
        activities = activities_response.json()
        participants = activities[test_activity]["participants"]
        assert test_email not in participants

    def test_unregister_nonexistent_activity_returns_404(self, client, invalid_activity, test_email):
        """
        Test that attempting to unregister from a non-existent activity returns 404.
        
        Arrange: Invalid activity name and test email
        Act: Make DELETE request with non-existent activity
        Assert: Verify 404 status and appropriate error message
        """
        # Arrange
        # (fixtures provide invalid_activity and test_email)

        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/unregister",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_student_not_enrolled_returns_400(self, client, test_activity, test_email):
        """
        Test that attempting to unregister a student not enrolled returns 400.
        
        Arrange: Test email that has not signed up for the activity
        Act: Make DELETE request for unenrolled student
        Assert: Verify 400 status and appropriate error message
        """
        # Arrange
        # (test_email fixture provides an email not signed up for any activity)

        # Act
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]
