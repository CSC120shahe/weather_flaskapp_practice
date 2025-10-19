*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BASE_URL}    http://localhost:5000
${USERNAME}    robot@example.com
${PASSWORD}    Password123!

*** Test Cases ***
Signup Test
    [Documentation]    This test verifies user signup functionality.
    Open Browser    ${BASE_URL}/signup    Chrome
    Input Text    id:username    ${USERNAME}
    Input Text    id:password    ${PASSWORD}
    Input Text    id:password2    ${PASSWORD}
    Click Button  xpath=//input[@value='Register']

Login Test
    [Documentation]    This test verifies user login functionality using the newly created user.
    Go To    ${BASE_URL}/login
    Input Text    id:username    ${USERNAME}
    Input Text    id:password    ${PASSWORD}
    Click Button    id:submit
    Wait Until Page Contains Element    xpath=//a[text()='Logout']

Select Option from Dropdown Test
    [Documentation]    This test verifies selecting an option from the dropdown menu on the index page.
    Wait Until Page Contains Element    id:weather-options
    Select From List By Value    weather-options    /weather_favorite_cities
    Wait Until Page Contains    Weather of Favorite Cities

Add Favorite City Test
    [Documentation]    This test verifies adding a favorite city.
    Go To    ${BASE_URL}/weather_favorite_cities
    Input Text    id:city_name    Raleigh
    Click Button    xpath=//input[@value='Add a new City']
    Wait Until Page Contains    Raleigh

Update City Note Test
    [Documentation]    This test verifies updating a city note.
    Go To    ${BASE_URL}/weather_favorite_cities
    Click Button    Edit Note
    Input Text Into Alert    text:This is a test note for Raleigh
    Handle Alert
    Wait Until Page Contains    This is a test note for Raleigh

Remove Favorite City Test
    [Documentation]    This test verifies removing a favorite city.
    Go To    ${BASE_URL}/weather_favorite_cities
    Click Button    xpath=//button[contains(text(), 'Remove City')]
    Handle Alert
    Handle Alert
    Wait Until Page Does Not Contain    Raleigh

Logout Test
    [Documentation]    This test verifies user logout functionality.
    Click Link    xpath=//a[text()='Logout']
    Wait Until Page Contains    Login
    Close Browser
