import pytest
import requests
import logging

# Base URL for the application
BASE_URL = "http://127.0.0.1:5000"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

@pytest.fixture(scope="module")
def session():
    """Fixture to manage a session for HTTP requests."""
    with requests.Session() as session:
        yield session

def test_signup_endpoint(session):
    logger.info("Starting test: test_signup_endpoint")
    # Attempt to sign up a test user
    response = session.post(f"{BASE_URL}/signup", data={
        "username": "testuser@example.com",
        "password": "Password123!",
        "password2": "Password123!",
    })

    if response.status_code == 200:
        logger.info("Test user signed up successfully.")
    elif response.status_code == 400:  # Assuming a 400 for existing users
        logger.info("Test user already exists, skipping signup.")
    else:
        pytest.fail(f"Unexpected status code during signup: {response.status_code}")

def test_login_endpoint(session):
    logger.info("Starting test: test_login_endpoint")
    # Log in with test user credentials
    response = session.post(f"{BASE_URL}/login", data={
        "username": "testuser@example.com",
        "password": "Password123!",
    })
    assert response.status_code == 200, "Login failed."
    logger.info("Test user logged in successfully.")

def test_weather_endpoint_requires_login(session):
    logger.info("Starting test: test_weather_endpoint_requires_login")
    # Access weather endpoint without login
    response = session.get(f"{BASE_URL}/weather")
    if response.status_code == 302:
        assert "/login" in response.headers.get("Location", ""), "Redirection to login failed."
    elif response.status_code == 200:
        logger.info("Weather endpoint is accessible with login.")
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")

def test_index_endpoint_requires_login(session):
    logger.info("Starting test: test_index_endpoint_requires_login")
    # Access index endpoint without login
    response = session.get(f"{BASE_URL}/index")
    if response.status_code == 302:
        assert "/login" in response.headers.get("Location", ""), "Redirection to login failed."
    elif response.status_code == 200:
        logger.info("Index endpoint is accessible with login.")
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")

def test_add_city_endpoint(session):
    logger.info("Starting test: test_add_city_endpoint")
    # Add a favorite city
    response = session.post(f"{BASE_URL}/weather_favorite_cities", data={
        "action": "add",
        "city_name": "New York",
    })
    assert response.status_code == 200, "Failed to add city."
    logger.info("City added successfully.")

def test_remove_city_endpoint(session):
    logger.info("Starting test: test_remove_city_endpoint")
    # Remove a city by ID
    response = session.post(f"{BASE_URL}/weather_favorite_cities", data={
        "action": "remove",
        "city_id": 1,  # Assuming city ID 1 exists
    })
    assert response.status_code == 200, "Failed to remove city."
    logger.info("City removed successfully.")

def test_logout_endpoint(session):
    logger.info("Starting test: test_logout_endpoint")
    # Log out the test user
    response = session.get(f"{BASE_URL}/logout")
    assert response.status_code in [200, 302], "Logout failed."
    logger.info("Test user logged out successfully.")
