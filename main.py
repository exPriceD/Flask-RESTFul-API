from config import application, db
from views import schedule, personalities, groups


if __name__ == "__main__":
    application.debug = True
    application.run()
    with application.app_context():
        db.create_all()
