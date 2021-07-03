import hashlib

from flask_login import UserMixin

from app import db, lm, app


class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    is_superuser = db.Column(db.Boolean, default=False)

    @staticmethod
    def hash_password(password):
        string = app.config["PASSWORD_SALT"] + password
        return hashlib.sha256(string.encode("utf-8")).hexdigest()

    def set_password(self, new_password):
        self.password = User.hash_password(new_password)

    def check_password(self, attempt):
        return User.hash_password(attempt) == self.password

    def __repr__(self):
        return f"User#{self.id}({self.username})"


@lm.user_loader
def load_user(id):
    return User.query.get(id)
