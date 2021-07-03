from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler


from config import Config
from ottd import SessionManager


app = Flask(__name__)
app.config.from_object(Config)

app.context_processor(lambda: dict(OTTD_SERVER_NAME=app.config["OTTD_SERVER_NAME"]))

db = SQLAlchemy(app)
lm = LoginManager(app)

scheduler = APScheduler()
scheduler.init_app(app)

sessions_manager = SessionManager(app, scheduler)
