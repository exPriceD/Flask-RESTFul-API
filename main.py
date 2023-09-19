from flask import request, Response
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email
from config import application, db
import json
import os
import typing as tp


@application.route('/api/v1/schedule', defaults={'group': None}, methods=["GET"])
@application.route('/api/v1/schedule/<string:group>', methods=["GET"])
def get_schedule_on_week(group):
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


@application.route('/api/v1/schedule/<string:group>/<int:week_number>', methods=["GET"])
def get_schedule_of_week_number(group, week_number):
    even_schedule, odd_schedule = get_schedule_json(group)
    if week_number % 2 == 0:
        response_data = {"even_week": even_schedule}
    else:
        response_data = {"odd_week": odd_schedule}
    return Response(
        response=json.dumps({"schedule": response_data}, ensure_ascii=False),
        status=200,
        mimetype='application/json',
    )


def get_schedule_json(group_name):
    with open(f"{os.getcwd()}\\groups\\{group_name}\\even_week.json", encoding='utf-8') as schedule_json:
        even_schedule = json.load(schedule_json)
    with open(f"{os.getcwd()}\\groups\\{group_name}\\odd_week.json", encoding='utf-8') as schedule_json:
        odd_schedule = json.load(schedule_json)
    return even_schedule, odd_schedule


if __name__ == "__main__":
    application.debug = True
    application.run()
