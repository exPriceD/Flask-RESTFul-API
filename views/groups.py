from flask import request, Response
from config import (application, db, GROUPS_KEYS)
from models import Groups
from utils import get_group_data
import json


@application.route('/api/v1/groups/', methods=["GET"])
def get_groups() -> Response:
    groups = Groups.query.all()
    response_data = {"data": {}}
    for group in groups:
        group_data = get_group_data(group=group)
        response_data["data"][group.name] = group_data
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/groups/<string:attr>/<string:attr_value>', methods=["GET"])
def get_groups_by_id(attr: str, attr_value: str) -> Response:
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


@application.route('/api/v1/groups/', methods=["POST"])
def add_group() -> Response:
    value = request.json
    request_keys = value.keys()
    if not all(key in request_keys for key in GROUPS_KEYS.keys()):
        resp = {"status": 400, "reason": "Поля заполнены некорректно"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    for key in request_keys:
        if value[key] and (len(str(value[key])) > GROUPS_KEYS[key]):
            resp = {"status": 400, "reason": f"Поле {key} превышает максимально возможную длину строки"}
            return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    group = Groups(name=value["name"], faculty=value["faculty"],
                   direction=value["direction"], people_count=value["people_count"])
    db.session.add(group)
    db.session.flush()
    db.session.refresh(group)
    db.session.commit()
    response_data = get_group_data(group=group)
    return Response(response=json.dumps(response_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/groups/<string:attr>/<string:attr_value>', methods=["PUT"])
def update_group(attr: str, attr_value: str) -> Response:
    value = request.json
    request_keys = value.keys()
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
    if not all(key in GROUPS_KEYS.keys() for key in request_keys):
        resp = {"status": 400, "reason": "Поля заполнены некорректно"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    for key in request_keys:
        if value[key] and (len(str(value[key])) > GROUPS_KEYS[key]):
            resp = {"status": 400, "reason": f"Поле {key} превышает максимально возможную длину строки"}
            return Response(response=json.dumps(resp, ensure_ascii=False), status=400, mimetype='application/json')
    try:
        if "name" in request_keys:
            group.fio = value["name"]
        if "faculty" in request_keys:
            group.faculty = value["faculty"]
        if "direction" in request_keys:
            group.direction = value["direction"]
        if "people_count" in request_keys:
            group.people_count = value["people_count"]
        db.session.commit()
        db.session.refresh(group)
    except Exception:
        resp = {"status": 500, "reason": "Непредвиденная ошибка при обновлении данных в БД"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=500, mimetype='application/json')
    person_data = get_group_data(group)
    return Response(response=json.dumps(person_data, ensure_ascii=False), status=200, mimetype='application/json')


@application.route('/api/v1/groups/<int:id>/', methods=["DELETE"])
def del_group(id: int) -> Response:
    group = Groups.query.filter_by(id=id).first()
    if not group:
        resp = {"status": 404, "reason": "Группа не найдена"}
        return Response(response=json.dumps(resp, ensure_ascii=False), status=404, mimetype='application/json')
    Groups.query.filter_by(id=id).delete()
    db.session.commit()
    return Response(response="Accepted", status=202, mimetype='application/json')