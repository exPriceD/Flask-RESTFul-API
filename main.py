from flask import request, Response
from validate_email import validate_email
from config import application, db
from models import Lessons, Personalities, Groups
from sqlalchemy import and_
import json
import os
import typing as tp

PERSONALITIES_KEYS = ["fio", "gender", "phone", "email", "work", "education"]
WEEKDAY = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
KEYS = ['id', 'email', 'phone']
PERSONALITIES_LENGTH = {"fio": 256, "gender": 6, "phone": 32, "email": 256, "work": 512, "education": 512}
SCHEDULE_KEYS = [
    "group", "day", "even_week", "subject", "type", "time_start",
    "time_end", "teacher_name", "room", "address", "zoom_url"
]
SCHEDULE_LENGTH = {
    "group": 6, "day": 16, "even_week": 1, "subject": 64, "type": 32, "time_start": 5,
    "time_end": 5, "teacher_name": 128, "room": 32, "address": 512, "zoom_url": 1024
}


@application.route('/api/v1/schedule/', methods=["GET"])
def get_schedule_on_week() -> Response:
    groups = Groups.query.all()
    response_data = {
        "data": {
            group.name: {
                "even_week": {day: [] for day in WEEKDAY},"odd_week": {day: [] for day in WEEKDAY}
            } for group in groups
        }
    }
    lessons = Lessons.query.all()
    for lesson in lessons:
        lesson_data = get_lessons_data(lesson)
        if lesson.even_week:
            response_data["data"][lesson.group]["even_week"][lesson.day].append(lesson_data)
        else:
            response_data["data"][lesson.group]["odd_week"][lesson.day].append(lesson_data)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/schedule/id/<int:id>/', methods=["GET"])
def get_schedule_by_id(id) -> Response:
    lesson = Lessons.query.filter_by(id=id).first()
    if not lesson:
        return Response(response="Not Found", status=404)
    lesson_data = get_lessons_data(lesson=lesson)
    if lesson.even_week:
        response_data = {"data": {lesson.group: {"even_week": {lesson.day: []}}}}
        response_data["data"][lesson.group]["even_week"][lesson.day].append(lesson_data)
    else:
        response_data = {"data": {lesson.group: {"odd_week": {lesson.day: []}}}}
        response_data["data"][lesson.group]["odd_week"][lesson.day].append(lesson_data)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/schedule/<string:group>/', methods=["GET"])
def get_schedule_for_group(group: str) -> Response:
    group = group.upper()
    lessons = Lessons.query.filter_by(group=group).all()
    if not lessons:
        return Response(response="Not Found", status=404)
    response_data = {
        "data": {
            group: {"even_week": {day: [] for day in WEEKDAY}, "odd_week": {day: [] for day in WEEKDAY}}
        }
    }
    for lesson in lessons:
        lesson_data = get_lessons_data(lesson)
        if lesson.even_week:
            response_data["data"][group]["even_week"][lesson.day].append(lesson_data)
        else:
            response_data["data"][group]["odd_week"][lesson.day].append(lesson_data)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/schedule/<string:group>/<string:week_number>/', methods=["GET"])
def get_schedule_of_week_number(group: str, week_number: str) -> Response:
    group = group.upper()
    week_number = week_number.upper()
    is_even, key, errors = check_week(week_number)
    if errors:
        resp = {"status": 400, "reason": "Некорректно заполненое поле WEEK"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    response_data = {"data": {group: {key: {day: [] for day in WEEKDAY}}}}
    lessons = Lessons.query.filter(and_(Lessons.group == group, Lessons.even_week == is_even)).all()
    for lesson in lessons:
        lesson_data = get_lessons_data(lesson)
        response_data["data"][group][key][lesson.day].append(lesson_data)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/schedule/<string:group>/<string:week_number>/<string:day>/', methods=["GET"])
def get_schedule_on_day(group: str, week_number: str, day: str) -> Response:
    group = group.upper()
    week_number = week_number.upper()
    day = day.lower()
    is_even, key, errors = check_week(week_number)
    if errors:
        resp = {"status": 400, "reason": "Некорректно заполненое поле WEEK"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    if not check_day(day):
        resp = {"status": 400, "reason": "Некорректно заполненое поле DAY"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    if day.isdigit():
        day = WEEKDAY[int(day)-1]
    response_data = {"data": {group: {key: {day: []}}}}
    lessons = Lessons.query.filter(and_(Lessons.group == group, Lessons.even_week == is_even, Lessons.day == day)).all()
    if not lessons:
        return Response(response="Lessons not Found", status=404)
    for lesson in lessons:
        lesson_data = get_lessons_data(lesson)
        response_data["data"][group][key][day].append(lesson_data)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/schedule/id/<int:id>/', methods=["PUT"])
def update_group_schedule(id) -> Response:
    value = request.json
    if not all(key in value.keys() for key in SCHEDULE_KEYS):
        resp = {"status": 400, "reason": "Поля заполнены некорректно"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    for key in value.keys():
        if len(str(value[key])) > SCHEDULE_LENGTH[key]:
            resp = {"status": 400, "reason": f"Поле {key} превышает максимально возможную длину строки"}
            return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    lesson = Lessons.query.filter_by(id=id).first()
    if not lesson:
        return Response("Not Found", status=404)
    try:
        lesson.group = value["group"]
        lesson.day = value["day"].lower()
        lesson.even_week = value["even_week"]
        lesson.subject = value["subject"]
        lesson.type = value["type"]
        lesson.time_start = value["time_start"]
        lesson.time_end = value["time_end"]
        lesson.teacher_name = value["teacher_name"]
        lesson.room = value["room"]
        lesson.address = value["address"]
        lesson.zoom_url = value["zoom_url"]
        db.session.commit()
    except Exception:
        resp = {"status": 500, "reason": "Непредвиденная ошибка при обновлении данных в БД"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=500, mimetype='application/json')
    return Response(response=json.dumps(value, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/schedule/', methods=["POST"])
def add_lessons():
    value = request.json
    if not all(key in value.keys() for key in SCHEDULE_KEYS):
        resp = {"status": 400, "reason": "Поля заполнены некорректно"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    for key in value.keys():
        if len(str(value[key])) > SCHEDULE_LENGTH[key]:
            resp = {"status": 400, "reason": f"Поле {key} превышает максимально возможную длину строки"}
            return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    group = Groups.query.filter_by(name=value["group"]).first()
    if not group:
        resp = {"status": 404, "reason": f"Группа {value['group']} не найдена!"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=404)
    lessons = Lessons(
        group=value["group"], day=value["day"], even_week=value["even_week"],
        subject=value["subject"], type=value["type"], time_start=value["time_start"],
        time_end=value["time_end"], teacher_name=value["teacher_name"],
        room=value["room"], address=value["address"], zoom_url=value["zoom_url"]
    )
    db.session.add(lessons)
    db.session.flush()
    db.session.commit()
    db.session.refresh(lessons)
    current_req = Lessons.query.filter_by(id=lessons.id).first()
    response_data = get_lessons_data(current_req)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype="application/json")


@application.route('/api/v1/schedule/id/<int:id>/', methods=["DELETE"])
def del_schedule(id: int) -> Response:
    lesson = Lessons.query.filter_by(id=id).first()
    if not lesson:
        return Response(response="Not Found", status=404)
    Lessons.query.filter_by(id=id).delete()
    db.session.commit()
    return Response(response="Accepted", status=202, mimetype='application/json')


@application.route('/api/v1/personalities/', methods=["GET"])
def get_person() -> Response:
    persons = Personalities.query.all()
    response_data = {"data": {}}
    for person in persons:
        person_data = get_person_data(person=person)
        response_data["data"][person.id] = person_data
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities/<string:attr>/<string:attr_value>/', methods=["GET"])
def get_person_by_id(attr: str, attr_value: str) -> Response:
    if attr not in KEYS:
        resp = {"status": 400, "reason": f"Атрибут {attr} не найден. Используйте атрибуты из списка: {KEYS}"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype="application/json")
    if attr == "id":
        person = Personalities.query.filter_by(id=int(attr_value)).first()
    elif attr == "email":
        person = Personalities.query.filter_by(email=attr_value).first()
    else:
        person = Personalities.query.filter_by(phone=attr_value).first()
    if not person:
        resp = {"status": 404, "reason": "Пользователь не найден"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=404, mimetype='application/json')
    person_data = get_person_data(person=person)
    response_data = {"data": {person.id: person_data}}
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities/', methods=["POST"])
def add_person():
    value = request.json
    request_keys = value.keys()
    if not all(key in PERSONALITIES_KEYS for key in request_keys):
        resp = {"status": 400, "reason": "Поля заполнены некорректно"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    if not validate_email(value["email"]):
        resp = {'status': 400, "reason": "Email not valid"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    person = Personalities(
        fio=value["fio"], gender=value["gender"], phone=value["phone"],
        email=value["email"], work=value["work"], education=value["education"]
    )
    db.session.add(person)
    db.session.flush()
    db.session.commit()
    person_data = get_person_data(person)
    return Response(response=json.dumps(person_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities/<string:attr>/<string:attr_value>/', methods=["PUT"])
def edit_person(attr: str, attr_value: str) -> Response:
    value = request.json
    request_keys = value.keys()
    if not all(key in PERSONALITIES_KEYS for key in request_keys):
        resp = {"status": 400, "reason": "Поля заполнены некорректно"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    for key in request_keys:
        if value[key] and (len(value[key]) > PERSONALITIES_LENGTH[key]):
            resp = {"status": 400, "reason": f"Поле {key} превышает максимально возможную длину строки"}
            return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    if attr not in KEYS:
        resp = {"status": 400, "reason": f"Атрибут {attr} не найден. Используйте атрибуты из списка: {KEYS}"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype="application/json")
    if attr == "id":
        person = Personalities.query.filter_by(id=int(attr_value)).first()
    elif attr == "email":
        person = Personalities.query.filter_by(email=attr_value).first()
    else:
        person = Personalities.query.filter_by(phone=attr_value).first()
    if not person:
        resp = {"status": 404, "reason": "Пользователь не найден"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=404, mimetype='application/json')
    try:
        if "fio" in request_keys:
            person.fio = value["fio"]
        if "gender" in request_keys:
            person.gender = value["gender"]
        if "phone" in request_keys:
            person.phone = value["phone"]
        if "email" in request_keys:
            person.email = value["email"]
        if "work" in request_keys:
            person.work = value["work"]
        if "education" in request_keys:
            person.education = value["education"]
        db.session.commit()
    except Exception:
        resp = {"status": 500, "reason": "Непредвиденная ошибка при обновлении данных в БД"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=500, mimetype='application/json')
    person_data = get_person_data(person)
    return Response(response=json.dumps(person_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities/<int:id>/', methods=["DELETE"])
def del_person(id):
    person = Personalities.query.filter_by(id=id).first()
    if not person:
        resp = {"status": 404, "reason": "Пользователь не найден"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=404, mimetype='application/json')
    Personalities.query.filter_by(id=id).delete()
    db.session.commit()
    return Response(response="Accepted", status=202, mimetype='application/json')


@application.route('/api/v1/groups/', methods=["GET"])
def get_groups():
    groups = Groups.query.all()
    response_data = {"data": {}}
    for group in groups:
        group_data = get_group_data(group=group)
        response_data["data"][group.name] = group_data
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/groups/<string:attr>/<string:attr_value>', methods=["GET"])
def get_groups_by_id(attr, attr_value):
    if attr == 'id' or attr == 'ID':
        group = Groups.query.filter_by(id=int(attr_value)).first()
    elif attr == 'name' or attr == 'NAME':
        group = Groups.query.filter_by(name=attr_value.upper()).first()
    else:
        resp = {"status": 400, "reason": f"Атрибут {attr} не найден. Используйте атрибуты: ['id', 'name']"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    if not group:
        resp = {"status": 404, "reason": "Группа не найдена"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=404, mimetype='application/json')
    group_data = get_group_data(group=group)
    response_data = {"data": {group.name: group_data}}
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


def get_lessons_data(lesson):
    lesson_data = {
        "id": lesson.id,
        "group": lesson.group,
        "day": lesson.day,
        "even_week": lesson.even_week,
        "subject": lesson.subject,
        "type": lesson.type,
        "time_start": lesson.time_start,
        "time_end": lesson.time_end,
        "teacher_name": lesson.teacher_name,
        "room": lesson.room,
        "address": lesson.address,
        "zoom_url": lesson.zoom_url
    }
    return lesson_data


def get_person_data(person):
    person_data = {
        "id": person.id,
        "fio": person.fio,
        "gender": person.gender,
        "phone": person.phone,
        "email": person.email,
        "work": person.work,
        "education": person.education
    }
    return person_data


def get_group_data(group):
    group_data = {
        "id": group.id,
        "name": group.name,
        "faculty": group.faculty,
        "direction": group.direction,
        "people_count": group.people_count
    }
    return group_data


def check_week(week_number):
    if not week_number.isdigit() and week_number != "EVEN" and week_number != "ODD":
        return None, None, True
    if week_number.isdigit():
        if int(week_number) < 1 or int(week_number) > 7:
            return None, None, True
        is_even, key = (1, "even_week") if int(week_number) % 2 == 0 else (0, "odd_week")
    else:
        is_even, key = (1, "even_week") if week_number == "EVEN" else (0, "odd_week")
    return is_even, key, False


def check_day(day):
    if not day.isdigit() and day not in WEEKDAY:
        return False
    if day.isdigit() and (int(day) < 1 or int(day) > 7):
        return False
    return True


if __name__ == "__main__":
    application.debug = True
    application.run()
    with application.app_context():
        db.create_all()
