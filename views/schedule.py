from flask import request, Response
from config import (application, db, WEEKDAY, SCHEDULE_LENGTH, SCHEDULE_KEYS)
from models import Lessons, Groups
from sqlalchemy import and_
from utils import get_lessons_data, check_week, check_day
import json
import datetime


@application.route('/api/v1/schedule/', methods=["GET"])
def get_schedule_on_week() -> Response:
    groups = Groups.query.all()
    response_data = {
        "data": {
            group.name: {
                "even_week": {day: [] for day in WEEKDAY}, "odd_week": {day: [] for day in WEEKDAY}
            } for group in groups
        }
    }
    lessons = Lessons.query.all()
    for lesson in lessons:
        lesson_data = get_lessons_data(lesson)
        if lesson.even_week:
            response_data["data"][lesson.group]["even_week"][lesson.day.lower()].append(lesson_data)
        else:
            response_data["data"][lesson.group]["odd_week"][lesson.day.lower()].append(lesson_data)
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


@application.route('/api/v1/schedule/name/<string:group>/', methods=["GET"])
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


@application.route('/api/v1/schedule/name/<string:group>/<string:week_number>/', methods=["GET"])
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


@application.route('/api/v1/schedule/name/<string:group>/<string:week_number>/<string:day>/', methods=["GET"])
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
    if not all(key in SCHEDULE_KEYS for key in value.keys()):
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
        if "group" in value.keys():
            group = Groups.query.filter_by(name=value["group"]).first()
            if not group:
                resp = {"status": 404, "reason": f"Группа {value['group']} не найдена"}
                return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
            lesson.group = value["group"]
        if "day" in value.keys():
            if value["day"].lower() not in WEEKDAY:
                resp = {"status": 400, "reason": f"Полe day заполнено некорректно. Используйте дни из набора {WEEKDAY}"}
                return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
            lesson.day = value["day"].lower()
        if "even_week" in value.keys():
            if int(value["even_week"]) not in [0, 1, True, False]:
                resp = {
                    "status": 400,
                    "reason": f"Полe even_week заполнено некорректно. Используйте {[0, 1, True, False]}"
                }
                return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
            lesson.even_week = value["even_week"]
        if "subject" in value.keys():
            lesson.subject = value["subject"]
        if "type" in value.keys():
            lesson.type = value["type"]
        if "time_start" in value.keys():
            try:
                if value["time_start"] != str(datetime.datetime.strptime(value["time_start"], "%H:%M"))[11:16]:
                    resp = {"status": 400, "reason": f"Полe time_start заполнено некорректно."}
                    return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
            except ValueError:
                resp = {"status": 400, "reason": f"Полe time_start заполнено некорректно."}
                return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
            lesson.time_start = value["time_start"]
        if "time_end" in value.keys():
            try:
                if value["time_end"] != str(datetime.datetime.strptime(value["time_end"], "%H:%M"))[11:16]:
                    resp = {"status": 400, "reason": f"Полe time_end заполнено некорректно."}
                    return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
            except ValueError:
                resp = {"status": 400, "reason": f"Полe time_end заполнено некорректно."}
                return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
            lesson.time_end = value["time_end"]
        if "teacher_name" in value.keys():
            lesson.teacher_name = value["teacher_name"]
        if "room" in value.keys():
            lesson.room = value["room"]
        if "address" in value.keys():
            lesson.address = value["address"]
        if "zoom_url" in value.keys():
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
    if value["day"].lower() not in WEEKDAY:
        resp = {"status": 400, "reason": f"Полe day заполнено некорректно. Используйте дни из набора {WEEKDAY}"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    if int(value["even_week"]) not in [0, 1, True, False]:
        resp = {
            "status": 400,
            "reason": f"Полe even_week заполнено некорректно. Используйте {[0, 1, True, False]}"
        }
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    try:
        if value["time_start"] != str(datetime.datetime.strptime(value["time_start"], "%H:%M"))[11:16]:
            resp = {"status": 400, "reason": f"Полe time_start заполнено некорректно."}
            return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    except ValueError:
        resp = {"status": 400, "reason": f"Полe time_start заполнено некорректно."}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    try:
        if value["time_end"] != str(datetime.datetime.strptime(value["time_end"], "%H:%M"))[11:16]:
            resp = {"status": 400, "reason": f"Полe time_end заполнено некорректно."}
            return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    except ValueError:
        resp = {"status": 400, "reason": f"Полe time_end заполнено некорректно."}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400)
    lessons = Lessons(
        group=value["group"], day=value["day"].lower(), even_week=value["even_week"],
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
