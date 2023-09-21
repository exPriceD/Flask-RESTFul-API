from config import db


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(6))
    faculty = db.Column(db.String(512))
    direction = db.Column(db.String(512))
    people_count = db.Column(db.Integer)

    def __repr__(self):
        return f"<Group {self.id} {self.name}>"


class Personalities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(256))
    gender = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(256))
    work = db.Column(db.String(512))
    education = db.Column(db.String(512))

    def __repr__(self):
        return f"<Person {self.id}>"


class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(6))
    day = db.Column(db.String(16))
    even_week = db.Column(db.Boolean)
    subject = db.Column(db.String(64))
    type = db.Column(db.String(32))
    time_start = db.Column(db.String(5))
    time_end = db.Column(db.String(5))
    teacher_name = db.Column(db.String(128))
    room = db.Column(db.String(32))
    address = db.Column(db.String(512))
    zoom_url = db.Column(db.String(1024))

    def __repr__(self):
        return f"Lessons {self.group}"



