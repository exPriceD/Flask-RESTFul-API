from flask import request, Response
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email
from config import application, db
import json
import os
import typing as tp

PERSONALITIES_KEYS = ("id", "fio", "gender", "phone", "email", "work", "education", "photo")


@application.route('/api/v1/schedule', defaults={'group': None}, methods=["GET"])
@application.route('/api/v1/schedule/<string:group>', methods=["GET"])
def get_schedule_on_week(group: str):
    response_data = {}
    if not group:
        groups = os.listdir(f"{os.getcwd()}\\groups")
        for group_name in groups:
            even_schedule, odd_schedule = get_schedule_json(group_name)
            response_data[group_name] = {"even_week": even_schedule, "odd_week": odd_schedule}
    else:
        try:
            even_schedule, odd_schedule = get_schedule_json(group)
        except OSError:
            return Response(
                response="Not Found",
                status=404,
            )
        response_data[group] = {"even_week": even_schedule, "odd_week": odd_schedule}
    return Response(
        response=json.dumps({"schedule": response_data}, ensure_ascii=False),
        status=200,
        mimetype='application/json',
    )


@application.route('/api/v1/schedule/<string:group>/<string:week_number>', methods=["GET"])
def get_schedule_of_week_number(group: str, week_number: str):
    even_schedule, odd_schedule = get_schedule_json(group)
    if week_number.isdigit():
        if int(week_number) % 2 == 0:
            response_data = {"even_week": even_schedule}
        else:
            response_data = {"odd_week": odd_schedule}
    elif week_number == "even":
        response_data = {"even_week": even_schedule}
    elif week_number == "odd":
        response_data = {"odd_week": odd_schedule}
    else:
        return Response(
            response="Week not Found",
            status=404,
        )
    return Response(
        response=json.dumps({"schedule": response_data}, ensure_ascii=False),
        status=200,
        mimetype='application/json',
    )


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
    return Response(response=json.dumps(value), status=200)


@application.route('/api/v1/personalities/<int:person_id>', methods=["PUT"])
def edit_person(person_id):
    value = request.json
    if not all(key in value.keys() for key in PERSONALITIES_KEYS):
        return Response(response=json.dumps({"status": 500, "reason": "Поля заполнены некорректно"}), status=500)
    with open(f"{os.getcwd()}\\personalities\\personalities.json", "r") as persons:
        personalities = json.load(persons)
    is_found = False
    for i, person in enumerate(personalities["data"], start=0):
        if person["id"] == person_id:
            personalities["data"][i] = value
            is_found = True
            break
    if not is_found:
        return Response(response={"status": 500, "reason": "Пользователь не найден"}, status=500)
    with open(f"{os.getcwd()}\\personalities\\personalities.json", "w") as persons:
        json.dump(personalities, persons, indent=4, ensure_ascii=False)
    return Response(response=json.dumps(value), status=200)


def get_schedule_json(group_name: str) -> tp.Tuple:
    with open(f"{os.getcwd()}\\groups\\{group_name}\\even_week.json", encoding='utf-8') as schedule_json:
        even_schedule = json.load(schedule_json)
    with open(f"{os.getcwd()}\\groups\\{group_name}\\odd_week.json", encoding='utf-8') as schedule_json:
        odd_schedule = json.load(schedule_json)
    return even_schedule, odd_schedule


if __name__ == "__main__":
    application.debug = True
    application.run()
