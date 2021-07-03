from os import environ
from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///web_rcon.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = environ.get("SECRET_KEY", "very_secret_key")
    PASSWORD_SALT = environ.get("PASSWORD_SALT", "very_secret_salt")

    OTTD_HOST = environ.get("OTTD_HOST", "127.0.0.1")
    OTTD_PORT = int(environ.get("OTTD_PORT", "3977"))
    OTTD_PASSWORD = environ.get("OTTD_PASSWORD", "123qwe")
    OTTD_SERVER_NAME = environ.get("OTTD_SERVER_NAME", "TestServer")
