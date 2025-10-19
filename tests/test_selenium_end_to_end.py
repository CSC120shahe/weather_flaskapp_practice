from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
service = Service()
driver = webdriver.Chrome(service=service)

# Reusable functions
def test_signup():
    try:
        driver.get("http://127.0.0.1:5000/signup")
        driver.find_element(By.NAME, "username").send_keys("hesha6@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "password2").send_keys("password123")
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)
        print("Signup test: Pass")
    except Exception as e:
        print("Signup test: Fail")
        print(f"Error: {e}")

def test_login():
    try:
        driver.get("http://127.0.0.1:5000/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("hesha6@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "submit").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
        print("Login test: Pass")
    except Exception as e:
        print("Login test: Fail")
        print(f"Error: {e}")

def test_add_city():
    try:
        driver.get("http://127.0.0.1:5000/weather_favorite_cities")
        city_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "city_name"))
        )
        city_input.send_keys("Raleigh")
        add_button = driver.find_element(By.XPATH, "//input[@value='Add a new City']")
        add_button.click()
        time.sleep(2)
        
        city_list = driver.find_elements(By.XPATH, "//li/h3")
        assert any("Raleigh" in city.text for city in city_list)
        print("Add city test: Pass")
    except Exception as e:
        print("Add city test: Fail")
        print(f"Error: {e}")

def test_remove_city():
    try:
        driver.get("http://127.0.0.1:5000/weather_favorite_cities")
        
        remove_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@method='post']//input[@value='Remove City']"))
        )
        remove_button.click()
        time.sleep(2)

        city_list = driver.find_elements(By.XPATH, "//li")
        assert len(city_list) == 0 
        print("Remove city test: Pass")
    except Exception as e:
        print("Remove city test: Fail")
        print(f"Error: {e}")

def test_update_note():
    try:
        driver.get("http://127.0.0.1:5000/weather_favorite_cities")
        
        edit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Edit Note')]"))
        )
        edit_button.click()
        
        # Handle the JavaScript prompt
        alert = driver.switch_to.alert
        alert.send_keys("Updated note for Raleigh")
        alert.accept()
        time.sleep(2)
        
        # Handle the success alert
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        success_alert = driver.switch_to.alert
        assert "City note updated successfully" in success_alert.text
        success_alert.accept()
        
        # Verify the updated note in the DOM
        updated_note = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li//p[contains(text(), 'Updated note for Raleigh')]"))
        )
        assert "Updated note for Raleigh" in updated_note.text
        print("Update note test: Pass")
    except Exception as e:
        print("Update note test: Fail")
        print(f"Error: {e}")

def test_logout():
    try:
        driver.get("http://127.0.0.1:5000/index")
        logout_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_link.click()
        time.sleep(2)
        print("Logout test: Pass")
    except Exception as e:
        print("Logout test: Fail")
        print(f"Error: {e}")

# Run the tests
test_signup()
test_login()
test_add_city()
test_update_note()
test_remove_city()
test_logout()

# Close the browser after tests
driver.quit()