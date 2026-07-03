import pytest
from fastapi.testclient import TestClient
from src.app import app

# Test data constants
TEST_EMAIL = "test.student@mergington.edu"
TEST_ACTIVITY = "Chess Club"
NONEXISTENT_ACTIVITY = "Nonexistent"
INVALID_EMAIL = "test@mergington.edu"


@pytest.fixture
def client():
    """Fixture that provides a TestClient instance for API testing."""
    return TestClient(app)


def test_get_activities_returns_activities(client):
    """Test that GET /activities returns all available activities."""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity in expected_activities:
        assert activity in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_returns_success_message(client):
    """Test that signing up for an existing activity returns a success message."""
    # Arrange
    email = TEST_EMAIL
    activity = TEST_ACTIVITY
    expected_message = f"Signed up {email} for {activity}"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}


def test_signup_for_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns a 404 error."""
    # Arrange
    email = INVALID_EMAIL
    activity = NONEXISTENT_ACTIVITY

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to the static index.html page."""
    # Arrange
    expected_location = "/static/index.html"
    expected_status_codes = (301, 307, 302)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in expected_status_codes
    assert response.headers["location"] == expected_location


def test_activity_response_structure(client):
    """Test that activity data contains all required fields."""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity_details in activities_data.items():
        for field in required_fields:
            assert field in activity_details, f"Field '{field}' missing from {activity_name}"
        assert isinstance(activity_details["participants"], list)
        assert isinstance(activity_details["max_participants"], int)


def test_signup_adds_participant_to_activity(client):
    """Test that signing up successfully adds a participant to an activity."""
    # Arrange
    new_email = "new.student@mergington.edu"
    activity = "Programming Class"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": new_email})
    activities_response = client.get("/activities")
    activities_data = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert new_email in activities_data[activity]["participants"]
