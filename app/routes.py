from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    render_template_string,
)
from app.forms import LoginForm, SignupForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from flask_mailman import EmailMessage
from app.templates.reset_password_email_content import (
    reset_password_email_html_content,
)
from app.models import User, City
from app import db
from urllib.parse import urlparse
from sqlalchemy import select
import requests


bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("main.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are now a registered user!")
        return redirect(url_for("main.login"))
    return render_template("signup.html", title="Register", form=form)


@bp.route("/weather", methods=["GET", "POST"])
@login_required
def weather():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        api_key = current_app.config["WEATHER_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            flash("City not found.")
    return render_template("weather.html", title="Weather", weather_data=weather_data)

@bp.route("/weather_favorite_cities", methods=["GET", "POST"])
@login_required
def weather_favorite_cities():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            city_name = request.form.get("city_name")
            if city_name:
                city = City.query.filter_by(name=city_name).first()
                if not city:
                    city = City(name=city_name)
                    db.session.add(city)
                    db.session.commit()
                if city not in current_user.favorite_cities:
                    current_user.favorite_cities.append(city)
                    db.session.commit()
                else:
                    flash("City already in your favorites.")
        return redirect(url_for("main.weather_favorite_cities"))

    favorite_cities = current_user.favorite_cities
    api_key = current_app.config["WEATHER_API_KEY"]
    weather_data_list = []

    for city in favorite_cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
           
            weather_data_list.append({
                "id": city.id,  
                "name": city.name,
                "temp": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"],
                "note":city.note
            })
        else:
            weather_data_list.append({
                "id": city.id,
                "name": city.name,
                "error": "Weather data not available",
                "note": city.note
            })

    return render_template("weather_favorite_cities.html", weather_data_list=weather_data_list)

@bp.route("/weather_favorite_cities/<city_id>", methods=["DELETE"])
@login_required
def delete_city(city_id):
    city = City.query.get(city_id)
    if not city or city not in current_user.favorite_cities:
        return {"error": "City not found or not in your favorites"}, 404
    
    current_user.favorite_cities.remove(city)
    db.session.delete(city)
    db.session.commit()
    return {"message": "City deleted successfully"}, 200

@bp.route("/weather_favorite_cities/<city_id>/note", methods=["PUT"])
@login_required
def update_city_note(city_id):
    city = City.query.get(city_id)
    if not city or city not in current_user.favorite_cities:
        return {"error": "City not found or not in favorites"}, 404
    note = request.json.get("note")
    if note:
        city.note = note
        db.session.commit()
        print("Note updated in database:", city.note)
        return {"message": "City note updated successfully"}, 200
    return {"error": "Note content is required"}, 400


@bp.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user_select = select(User).where(User.username == form.email.data)
        user = db.session.scalar(user_select)

        if user:
            send_reset_password_email(user)

        flash(
            "Instructions to reset your password were sent to your email address,"
            " if it exists in our system."
        )

        return redirect(url_for("main.reset_password_request"))

    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


def send_reset_password_email(user):
    reset_password_url = url_for(
        "main.reset_password",
        token=user.generate_reset_password_token(),
        user_id=user.id,
        _external=True,
    )

    email_body = render_template_string(
        reset_password_email_html_content, reset_password_url=reset_password_url
    )

    message = EmailMessage(
        subject="Reset your password",
        body=email_body,
        to=[user.username],
    )
    message.content_subtype = "html"

    message.send()


@bp.route("/reset_password/<token>/<int:user_id>", methods=["GET", "POST"])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = User.validate_reset_password_token(token, user_id)
    if not user:
        return render_template(
            "reset_password_error.html", title="Reset Password error"
        )

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()

        return render_template(
            "reset_password_success.html", title="Reset Password success"
        )

    return render_template("reset_password.html", title="Reset Password", form=form)

