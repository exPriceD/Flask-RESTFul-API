from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

application = Flask(__name__)
application.config.from_object(__name__)

application.secret_key = "8b5ad1a5811c417dfc5ca02f1eac1b17bae6a4f1859320bde495f74ab5d821db"
application.permanent_session_lifetime = timedelta(days=365)

application.config['UPLOAD_FOLDER'] = 'uploads'
application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(application)