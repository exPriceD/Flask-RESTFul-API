from flask import request, Response
from validate_email import validate_email
from config import (application, db, KEYS, PERSONALITIES_KEYS, PERSONALITIES_LENGTH)
from models import Personalities
from utils import get_person_data
import json


@application.route('/api/v1/personalities/', methods=["GET"])
def get_person() -> Response:
    persons = Personalities.query.all()
    response_data = {"data": {}}
    for person in persons:
        person_data = get_person_data(person=person)
        response_data["data"][person.id] = person_data
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/personalities/<string:attr>/<string:attr_value>/', methods=["GET"])
def get_person_by_attr(attr: str, attr_value: str) -> Response:
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
    db.session.refresh(person)
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
        if value[key] and (len(str(value[key])) > PERSONALITIES_LENGTH[key]):
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
def del_person(id: int) -> Response:
    person = Personalities.query.filter_by(id=id).first()
    if not person:
        resp = {"status": 404, "reason": "Пользователь не найден"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=404, mimetype='application/json')
    Personalities.query.filter_by(id=id).delete()
    db.session.commit()
    response_data = {"status": 202, "message": "Accepted"}
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=202, mimetype='application/json')
