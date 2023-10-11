from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

application = Flask(__name__)
application.config.from_object(__name__)

application.secret_key = os.getenv("SECRET_KEY")
application.permanent_session_lifetime = timedelta(days=365)

application.config['UPLOAD_FOLDER'] = 'uploads'
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(application)

PERSONALITIES_KEYS = ["fio", "gender", "phone", "email", "work", "education"]
WEEKDAY = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
KEYS = ['id', 'email', 'phone']
PERSONALITIES_LENGTH = {"fio": 256, "gender": 6, "phone": 32, "email": 256, "work": 512, "education": 512}
SCHEDULE_KEYS = [
    "group", "day", "even_week", "subject", "type", "time_start",
    "time_end", "teacher_name", "room", "address", "zoom_url"
]
SCHEDULE_LENGTH = {
    "group": 6, "day": 16, "even_week": 5, "subject": 64, "type": 32, "time_start": 5,
    "time_end": 5, "teacher_name": 128, "room": 32, "address": 512, "zoom_url": 1024
}
GROUPS_KEYS = {"name": 6, "faculty": 512, "direction": 512, "people_count": 1000}
