import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "you-will-never-guess"
    )  # Replace with a strong secret key
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")  # Set this environment variable

    MAIL_BACKEND = "console"
    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = "noreply@weatherapp.com"

class TestConfig(Config):
    TESTING = True
    # Use an in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Disable CSRF protection for testing
    WTF_CSRF_ENABLED = False
    # Override mail backend to prevent sending actual emails during testing
    MAIL_BACKEND = "dummy"
    MAIL_DEFAULT_SENDER = "noreply@test.com"
