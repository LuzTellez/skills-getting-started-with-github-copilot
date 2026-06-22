"""
Pytest configuration and fixtures for FastAPI tests.

This module provides shared fixtures for all tests in the suite.
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


# Store the original activities state for resetting between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team for practice and matches",
        "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Improve swimming techniques and compete in swim meets",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["sophia@mergington.edu", "lucas@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
    },
    "Drama Club": {
        "description": "Develop acting skills and rehearse for school theater productions",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "liam@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking and argumentation for competitions",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["olivia@mergington.edu", "mason@mergington.edu"]
    },
    "Science Club": {
        "description": "Investigate science topics through experiments and projects",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "noah@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets the activities dictionary to its original state before each test.
    
    This ensures test isolation by clearing any modifications made by previous tests.
    autouse=True means this fixture runs automatically for every test without needing
    to explicitly request it.
    """
    # Reset activities to original state using deep copy to ensure complete isolation
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for making requests to the FastAPI app.
    
    The TestClient automatically handles the test lifecycle and allows us to make
    HTTP requests to the app without running a live server.
    """
    return TestClient(app_module.app)


@pytest.fixture
def test_email():
    """Fixture providing a test email that is not already signed up for activities."""
    return "test_student@mergington.edu"


@pytest.fixture
def test_activity():
    """Fixture providing a valid activity name for testing."""
    return "Chess Club"


@pytest.fixture
def invalid_activity():
    """Fixture providing an invalid activity name that does not exist."""
    return "Non-existent Activity"
