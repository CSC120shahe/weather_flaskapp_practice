# Weather Forecast Application

## Introduction or Background
A web application that displays weather information for a specified location. The application utilizes the OpenWeatherMap API to retrieve weather data.

## Team Members
- Sha He (Group Lead)
- Jaylan Chavis
- Corey Devolld
- Anthony De Casas Mata
- Ryan Burres (withdrew from course)
- Nicholas E. Pacejka

## Overview
This project is a Flask-based web application that allows users to manage their favorite cities' weather information. Users can create accounts, log in, add/remove favorite cities, update city notes, and view detailed weather data. The project also implements comprehensive testing and test coverage to ensure functionality.

## Features
- **User Authentication**:
  - Signup and Login functionality with validation.
  - Password reset via email.
- **Weather Management**:
  - Add and remove favorite cities.
  - View weather details, including temperature, humidity, wind speed, and descriptions.
  - Add and update custom notes for each city.
- **Weather Forecast**:
  - View weather forecast for the selected location.
- **Notifications**:
  - Email or in-app notifications for updates.
- **Testing and Automation**:
  - Unit tests, API tests, UI tests, and acceptance tests implemented.
  - Test coverage report available.

## Installation Instructions

### Prerequisites
- Python 3.8+
- `pip` package manager

### Project Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/csc256/fa24project-fa24project_team2.git
   cd fa24project-fa24project_team2
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Set Environment Variables:
   For Unix/Linux/Mac:
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export SECRET_KEY='your-secret-key'  # Replace with a strong secret key
   export WEATHER_API_KEY='your-openweathermap-api-key'
   ```

   For Windows:
   ```bash
   set FLASK_APP=run.py
   set FLASK_ENV=development
   set SECRET_KEY='your-secret-key'  # Replace with a strong secret key
   set WEATHER_API_KEY='your-openweathermap-api-key'
   ```
   Go to [OpenWeatherMap API](https://openweathermap.org/api) to register and get your own WEATHER_API_KEY.

5. [Notice: Only needed for the 1st time] This step helps you create a user table in your local database:
   ```bash
   flask db upgrade
   ```

6. Run the flask app:
   ```bash
   flask run
   ```
   The application will be accessible at [http://localhost:5000](http://localhost:5000).

7. [Optional] If you have changed `app/models.py`, run the following commands to generate and apply a schema migration script:
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

## Usage Instructions
- Log in or sign up to access the weather dashboard.
- Add or remove cities to your favorites list.
- Update notes for any city.
- View weather forecasts and current conditions for your selected locations.

## Technology Stack
- **Framework**: Flask
- **Language**: Python
- **Testing Frameworks**: pytest, Selenium, Robot Framework

## Features and Functionality
- **User Authentication**: Sign up, login, password reset
- **Location Selection**: Select a location to display weather information
- **Weather Forecast**: View weather forecast for the selected location
- **Notifications**: Email or in-app notifications for updates

## Contribution Guidelines
- **Coding Standards**: Follow PEP 8.
- **Branch Naming**: Use descriptive names (e.g., `feature-login`, `bugfix-db-error`).
- **Pull Request Process**:
  1. Fork the repository.
  2. Create a feature branch:
     ```bash
     git checkout -b feature-name
     ```
  3. Commit changes:
     ```bash
     git commit -m "Add a meaningful commit message"
     ```
  4. Push to the branch:
     ```bash
     git push origin feature-name
     ```
  5. Open a Pull Request.

## Testing Procedures
This project includes a comprehensive test plan to ensure functionality, security, and reliability. For detailed information, please refer to the full test plan [here](docs/test/test-plan-v1.md).

### Key Points
- **Unit Testing**: Using Pytest for individual components.
- **Integration Testing**: Ensuring interaction between frontend and backend.
- **UI Testing**: Using Selenium and Playwright.
- **Performance Testing**: Using Locust or k6.
- **API Testing**: Using Postman.
- **Robot Framework Testing**: For UI, database interactions, and REST APIs.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact Information
For questions or support, please contact the team members via the GitHub repository.

## Acknowledgments
- [OpenWeatherMap API](https://openweathermap.org/api) for weather data.

## Version History/Changelog
- **v1.0**: Initial project setup with core features.
- **v1.1**: Added test coverage tools and API integration.

## Frequently Asked Questions (FAQs)
### How do I get an OpenWeatherMap API key?
Register on [OpenWeatherMap API](https://openweathermap.org/api) and create a free account to generate an API key.

### What are the system requirements?
Python 3.8 or higher and `pip` installed on your system.
