from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from config import Config



user_cities = db.Table('user_cities',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('city_id', db.Integer, db.ForeignKey('city.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    favorite_cities = db.relationship(
        "City", 
        secondary=user_cities, 
        backref=db.backref("users", lazy="dynamic")
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_password_token(self):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        return serializer.dumps(self.username, salt=self.password_hash)

    @staticmethod
    def validate_reset_password_token(token: str, user_id: int):
        user = db.session.get(User, user_id)

        if user is None:
            return None

        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            token_user_email = serializer.loads(
                token,
                max_age=900,  # 15 minutes
                salt=user.password_hash,
            )
        except (BadSignature, SignatureExpired):
            return None

        if token_user_email != user.username:
            return None

        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    note = db.Column(db.String(128), nullable=True) 

    def __repr__(self):
        return f'<City {self.name}>'
