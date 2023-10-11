import requests


def personalities_post():
    json_data = {
        "id": 2,
        "fio": "Лукичева Алиса Юрьевна",
        "gender": "female",
        "phone": "+79114223909",
        "email": "479573@edu.itmo.ru",
        "work": None,
        "education": None,
    }
    url = "http://127.0.0.1:5000/api/v1/personalities"
    res = requests.post(url=url, json=json_data)
    return print(res, res.json())


def personalities_put():
    json_data = {
        "fio": "Лукичева Алиса Юрьевна",
        "gender": "female111111",
        "phone": "+79114223909",
        "email": "479573@edu.itmo.ru",
        "work": None,
        "education": None,
    }
    url = "http://127.0.0.1:5000/api/v1/personalities/2"
    res = requests.put(url=url, json=json_data)
    return print(res, res.json())


def schedule_put():
    json_data = {
        "group": "M3117",
        "day": "Friday",
        "even_week": 1,
        "subject": "Информатика",
        "type": "Лекция",
        "time_start": "10:00",
        "time_end": "11:30",
        "teacher_name": "Добриборщ Дмитрий",
        "room": "2433",
        "address": "Кронверкский пр., д.49, лит.А",
        "zoom_url": None,
    }
    url = "http://127.0.0.1:5000/api/v1/schedule/id/3"
    res = requests.put(url=url, json=json_data)
    return print(res, res.json())


#personalities_post()
personalities_put()
#schedule_put()
