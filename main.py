from flask import request, Response
from validate_email import validate_email
from config import application, db
from models import Lessons, Personalities, Groups
import json
import os
import typing as tp

PERSONALITIES_KEYS = ("id", "fio", "gender", "phone", "email", "work", "education")
WEEKDAY = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


@application.route('/api/v1/schedule', methods=["GET"])
def get_schedule_on_week():
    groups = Groups.query.all()
    response_data = {
        "data": {group.name: {"even_week": {day: [] for day in WEEKDAY},
                              "odd_week": {day: [] for day in WEEKDAY}} for group in groups}}
    print(response_data)
    lessons = Lessons.query.all()
    for lesson in lessons:
        lesson_data = get_lessons_data(lesson)
        if lesson.even_week:
            response_data["data"][lesson.group]["even_week"][lesson.day].append(lesson_data)
        else:
            response_data["data"][lesson.group]["odd_week"][lesson.day].append(lesson_data)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/schedule/<string:group>', methods=["GET"])
def get_schedule_for_group(group: str):
    group = group.upper()
    lessons = Lessons.query.filter_by(group=group).all()
    if not lessons:
        return Response(response="Not Found", status=404)
    response_data = {"data":
                         {group: {"even_week": {day: [] for day in WEEKDAY}, "odd_week": {day: [] for day in WEEKDAY}}}
                     }
    for lesson in lessons:
        lesson_data = get_lessons_data(lesson)
        if lesson.even_week:
            response_data["data"][group]["even_week"][lesson.day].append(lesson_data)
        else:
            response_data["data"][group]["odd_week"][lesson.day].append(lesson_data)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/schedule/<string:group>/<string:week_number>', methods=["GET"])
def get_schedule_of_week_number(group: str, week_number: str):
    even_schedule, odd_schedule = get_schedule_json(group)
    if week_number.isdigit():
        response_data = {"even_week": even_schedule} if int(week_number) % 2 == 0 else {"odd_week": odd_schedule}
    elif week_number == "even":
        response_data = {"even_week": even_schedule}
    elif week_number == "odd":
        response_data = {"odd_week": odd_schedule}
    else:
        return Response(response="Week not Found", status=404, )
    return Response(response=json.dumps({response_data}, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities', methods=["GET"])
def get_person():
    with open(f"{os.getcwd()}\\personalities\\personalities.json", "r") as persons:
        personalities = json.load(persons)
    return Response(response=json.dumps(personalities, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities/<int:person_id>', methods=["GET"])
def get_person_by_id(person_id: int):
    with open(f"{os.getcwd()}\\personalities\\personalities.json", "r") as persons:
        personalities = json.load(persons)
    is_found = False
    search_person = {}
    for i, person in enumerate(personalities["data"], start=0):
        if int(person["id"]) == person_id:
            search_person = person
            is_found = True
            break
    if not is_found:
        resp = {"status": "500", "reason": "Пользователь не найден"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=500, mimetype='application/json')
    return Response(response=json.dumps(search_person, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities', methods=["POST"])
def add_person():
    value = request.json
    if not all(key in value.keys() for key in PERSONALITIES_KEYS):
        return Response(response=json.dumps({"status": 500, "reason": "Поля заполнены некорректно"}), status=500)
    with open(f"{os.getcwd()}\\personalities\\personalities.json", "r") as persons:
        personalities = json.load(persons)
    personalities["data"].append(value)
    with open(f"{os.getcwd()}\\personalities\\personalities.json", "w") as persons:
        json.dump(personalities, persons, indent=4, ensure_ascii=False)
    return Response(response=json.dumps(value, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities/<int:person_id>', methods=["PUT"])
def edit_person(person_id: int):
    value = request.json
    if not all(key in value.keys() for key in PERSONALITIES_KEYS):
        resp = {"status": 500, "reason": "Поля заполнены некорректно"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=500, mimetype='application/json')
    with open(f"{os.getcwd()}\\personalities\\personalities.json", "r") as persons:
        personalities = json.load(persons)
    is_found = False
    for i, person in enumerate(personalities["data"], start=0):
        if int(person["id"]) == person_id:
            personalities["data"][i] = value
            is_found = True
            break
    if not is_found:
        resp = {"status": "500", "reason": "Пользователь не найден"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=500, mimetype='application/json')
    with open(f"{os.getcwd()}\\personalities\\personalities.json", "w") as persons:
        json.dump(personalities, persons, indent=4, ensure_ascii=False)
    return Response(response=json.dumps(value, ensure_ascii=False), status=200, mimetype='application/json')


def get_schedule_json(group_name: str) -> tp.Tuple:
    with open(f"{os.getcwd()}\\groups\\{group_name}\\even_week.json", encoding='utf-8') as schedule_json:
        even_schedule = json.load(schedule_json)
    with open(f"{os.getcwd()}\\groups\\{group_name}\\odd_week.json", encoding='utf-8') as schedule_json:
        odd_schedule = json.load(schedule_json)
    return even_schedule, odd_schedule


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

if __name__ == "__main__":
    application.debug = True
    application.run()
    with application.app_context():
        db.create_all()
