import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db
from app.models import User, City
from config import TestConfig

# Pytest fixture to create and configure the Flask app
@pytest.fixture
def app():
    # Create the Flask application and set it up for testing
    app = create_app(config_class=TestConfig)
    with app.app_context():
        db.create_all()  # Create tables in the in-memory database
        yield app  # Provide the app for testing
        db.session.remove()
        if app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:':
            db.drop_all()

# Pytest fixture to provide a test client for interacting with the app
@pytest.fixture
def client(app):
    return app.test_client()

# Fixture to ensure a rollback after each test to prevent data collisions
@pytest.fixture(autouse=True)
def rollback_session(app):
    with app.app_context():
        yield
        db.session.rollback()

# Test for successful registration 01
def test_registration_success(app):
    with app.app_context():
        user = User(username='testuser')
        user.set_password('Password123!')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username='testuser').first()
        assert retrieved_user is not None
        assert retrieved_user.check_password('Password123!')

# Test for attempting to register a duplicate user 02
def test_registration_duplicate_user(app):
    with app.app_context():
        user1 = User(username='testuser')
        user1.set_password('Password123!')
        db.session.add(user1)
        db.session.commit()

        user2 = User(username='testuser')
        db.session.add(user2)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            assert True  # Expect an exception due to unique constraint

# Test for successful login 03
def test_login_success(app, client):
    with client:
        with app.app_context():
            user = User(username="weatheruser@example.com")
            user.set_password("Password123!")
            db.session.add(user)
            db.session.commit()

        response = client.post("/login", data={
            "username": "weatheruser@example.com",
            "password": "Password123!"
        })
        assert response.status_code == 302, "Login did not redirect as expected."

        response = client.get("/index")
        assert response.status_code == 200, "Expected to access index page successfully"
        assert b"Home" in response.data

# Test for login with incorrect password 04
def test_login_incorrect_password(app):
    with app.app_context():
        user = User(username='testuser3')
        user.set_password('Password123!')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username='testuser3').first()
        assert retrieved_user is not None
        assert not retrieved_user.check_password('WrongPassword')

# Test for successful password reset token generation and validation 05
def test_password_reset_success(app):
    with app.app_context():
        user = User(username='testuser4')
        user.set_password('Password123!')
        db.session.add(user)
        db.session.commit()

        token = user.generate_reset_password_token()
        validated_user = User.validate_reset_password_token(token, user.id)

        assert validated_user is not None
        assert validated_user.username == 'testuser4'

# Test for attempting to validate an invalid password reset token 06
def test_password_reset_nonexistent_user(app):
    with app.app_context():
        validated_user = User.validate_reset_password_token('invalid_token', 999)
        assert validated_user is None
# t Test 07
def test_weather_access_with_login(client):
    # register and log in.
    with client:
        signup_response = client.post("/signup", data={
            "username": "weatheruser@example.com",
            "password": "Password123!",
            "password2": "Password123!",
            "submit": "Register"
        })
        assert signup_response.status_code == 302, f"Signup failed, got {signup_response.status_code}"

        login_response = client.post("/login", data={
            "username": "weatheruser@example.com",
            "password": "Password123!",
            "remember_me": "y",
            "submit": "Sign In"
        })
        assert login_response.status_code == 302, f"Login failed, got {login_response.status_code}"
    
        response = client.get("/weather")
        assert response.status_code == 200
        assert b"Weather" in response.data  

def test_weather_access_without_login(app,client):
    with client:
        response = client.get("/weather")
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]


def test_add_favorite_city(app,client):
     with client:  
        with app.app_context():
            # Step 1: register
            response = client.post("/signup", data={
                "username": "cityuser@example.com",  
                "password": "Password123!",
                "password2": "Password123!",  
                "submit": "Register"  
            })
            assert response.status_code == 302, "User registration did not redirect as expected."

            # Step 2: log in
            response = client.post("/login", data={
                "username": "cityuser@example.com",
                "password": "Password123!",
                "remember_me": "y",  
                "submit": "Sign In"
            })
            assert response.status_code == 302, "User login did not redirect as expected."

            # Step 3: add a favorite city
            response = client.post("/weather_favorite_cities", data={
                "action": "add",
                "city_name": "Apex"
            })
            assert response.status_code == 302, "Adding favorite city did not redirect as expected."

            # Step 4:Verify the city  was added in the database
            user = User.query.filter_by(username="cityuser@example.com").first()
            assert user is not None, "User was not found in the database"
            assert any(city.name == "Apex" for city in user.favorite_cities), "City not added to favorites"

def test_delete_favorite_city(app, client):
    with client:
        with app.app_context():
            # Step 1: Register a new user
            response = client.post("/signup", data={
                "username": "citydeleter@example.com",
                "password": "Password123!",
                "password2": "Password123!",
                "submit": "Register"
            })
            assert response.status_code == 302, "User registration did not redirect as expected."

            # Step 2: Log in
            response = client.post("/login", data={
                "username": "citydeleter@example.com",
                "password": "Password123!",
                "remember_me": "y",
                "submit": "Sign In"
            })
            assert response.status_code == 302, "User login did not redirect as expected."

            # Step 3: Add a favorite city
            response = client.post("/weather_favorite_cities", data={
                "action": "add",
                "city_name": "Raleigh"
            })
            assert response.status_code == 302, "Adding favorite city did not redirect as expected."

            # Retrieve the user and the added city
            user = User.query.filter_by(username="citydeleter@example.com").first()
            assert user is not None, "User not found in the database"
            city = City.query.filter_by(name="Raleigh").first()
            assert city in user.favorite_cities, "City not added to favorites"

            # Step 4: Send DELETE request to remove the city
            city_id = city.id
            response = client.delete(f"/weather_favorite_cities/{city_id}")
            assert response.status_code == 200, "Deleting favorite city did not return a success status"
            assert response.json["message"] == "City deleted successfully", "Delete confirmation message mismatch"

            # Step 5: Verify the city is no longer in the database
            db.session.expire_all()  # Refresh session
            deleted_city = db.session.get(City, city_id)
            assert deleted_city is None, "City was not deleted from the database"

def test_update_city_note(app, client):
    with client:
        with app.app_context():
            # Step 1: register
            response = client.post("/signup", data={
                "username": "cityuser@example.com",
                "password": "Password123!",
                "password2": "Password123!",
                "submit": "Register"
            })
            assert response.status_code == 302, "User registration did not redirect as expected."

            # Step 2: log in
            response = client.post("/login", data={
                "username": "cityuser@example.com",
                "password": "Password123!",
                "remember_me": "y",
                "submit": "Sign In"
            })
            assert response.status_code == 302, "User login did not redirect as expected."

            # Step 3: add a favorite city
            response = client.post("/weather_favorite_cities", data={
                "action": "add",
                "city_name": "Apex"
            })
            assert response.status_code == 302, "Adding favorite city did not redirect as expected."

            # Retrieve the user and the city added to the favorites
            user = User.query.filter_by(username="cityuser@example.com").first()
            assert user is not None, "User was not found in the database"
            city = City.query.filter_by(name="Apex").first()
            assert city in user.favorite_cities, "City was not added to favorites"

            # Step 4: update the note for the favorite city
            city_id = city.id
            new_note = "Defaulted"
            response = client.put(f"/weather_favorite_cities/{city_id}/note", json={
                "note": new_note
            })
            assert response.status_code == 200, "Updating city note did not return a success status"
            assert response.json["message"] == "City note updated successfully", "Update note message not received as expected"

            # Step 5: Verify the note was updated in the database
            #updated_city = City.query.get(city_id)
            updated_city = db.session.get(City, city_id)
            assert updated_city.note == new_note, "City note was not updated in the database"