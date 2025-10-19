import pytest
from playwright.sync_api import sync_playwright
import os
import time


@pytest.fixture(scope="session")
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        # context = browser.new_context()
        # page = context.new_page()
        page = browser.new_page()
        yield page
        browser.close()

def test_signup(page):
    try:
        page.goto("http://127.0.0.1:5000/signup", timeout=60000)
        page.wait_for_load_state()
        page.fill("input#username", "") 
        page.wait_for_selector("input#username:enabled") 
        page.fill("input[name='username']", "testuser@example.com")
        page.fill("input#password", "")
        page.wait_for_selector("input#password:enabled")
        page.fill("input[name='password']", "password123")
        page.fill("input[name='password2']", "password123")
        page.click("input[name='submit']")
        page.wait_for_timeout(2000)
        print("Signup test passed.")
    except Exception as e:
        print(f"Signup test failed. Error: {str(e)}")
        raise

def login(page, username, password):
    page.goto("http://127.0.0.1:5000/login")
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("input[name='submit']")
    page.wait_for_selector("text=Logout", timeout=60000)
    try:
        page.wait_for_selector("text=Logout", timeout=5000)
        return "success"
    except:
        if page.is_visible("ul.flashes li"):
            return "failure"
        raise Exception("Unexpected behavior during login")

def test_login_valid(page):
    login(page, "testuser@example.com", "password123")
    print("Login with valid credentials passed.")


@pytest.mark.parametrize("city_name", ["Morrisville", "New York", "12"])
def test_get_weather(page, city_name):
    page.goto("http://127.0.0.1:5000/weather")
    page.fill("input[name='city']", city_name)
    page.click("input[type='submit']")
    if city_name == "12":
        assert page.is_visible("text=City not found"), "Error message not shown for invalid city"
    else:
        assert page.is_visible(f"h2:has-text('Weather in {city_name}')"), f"Weather not displayed for {city_name}"

def test_add_new_city(page):
    try:
        page.goto("http://127.0.0.1:5000/weather_favorite_cities", timeout=60000)
        page.wait_for_selector("h1")
        new_city_name = "Raleigh"
        if page.is_visible(f"h3:has-text('{new_city_name}')"):
            print(f"City '{new_city_name}' already exists. Skipping addition.")
        else:
            page.fill("input#city_name", new_city_name)
            page.click("input[value='Add a new City']")
            page.wait_for_timeout(2000)
            assert page.is_visible(f"h3:has-text('{new_city_name}')"), f"City '{new_city_name}' not found in the list"
        print("Add new city test passed.")
    except Exception as e:
        print(f"Add new city test failed. Error: {str(e)}")
        raise

def test_remove_city(page):
    try:
        page.goto("http://127.0.0.1:5000/weather_favorite_cities", timeout=60000)
        page.wait_for_selector("h1")
        city_name = "Cary"
        page.fill("input#city_name", city_name)
        page.click("input[value='Add a new City']")
        page.wait_for_timeout(2000)

        # Handle dialog during remove
        page.on("dialog", lambda dialog: dialog.accept())
        page.click(f"//h3[contains(text(), '{city_name}')]/following-sibling::button[contains(text(), 'Remove City')]")
        page.wait_for_timeout(4000)
        assert not page.is_visible(f"h3:has-text('{city_name}')"), f"City '{city_name}' was not removed successfully"
        print("Remove city test passed.")
    except Exception as e:
        print(f"Remove city test failed. Error: {str(e)}")
        raise

def test_logout(page):
    try:
        page.goto("http://127.0.0.1:5000/index", timeout=60000)
        page.wait_for_selector("h1")
        assert page.is_visible("a[href='/logout']"), "Logout link not found"
        page.click("a[href='/logout']")
        page.wait_for_url("http://127.0.0.1:5000/login", timeout=60000)
        assert "Sign In" in page.text_content("h1"), "Logout failed or incorrect redirection"
        print("Logout test passed.")
    except Exception as e:
        print(f"Logout test failed. Error: {str(e)}")
        raise