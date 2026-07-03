from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_returns_success_message():
    email = "test.student@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_signup_for_nonexistent_activity_returns_404():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (301, 307, 302)
    assert response.headers["location"] == "/static/index.html"
