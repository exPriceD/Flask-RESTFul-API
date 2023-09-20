import requests


def personalities_post():
    json_data = {
        "id": 4,
        "fio": "Van Den Berg Cornelis A.T. (Nico) ",
        "gender": "male",
        "phone": None,
        "email": "c.a.t.vandenberg@umcutrecht.nl",
        "work": None,
        "education": None,
        "photo": None
    }
    url = "http://127.0.0.1:5000/api/v1/personalities"
    res = requests.post(url=url, json=json_data)
    return print(res, res.json())


def schedule_put():
    json_data = {
        "group": "M3117",
        "day": "Friday",
        "even_week": 1,
        "subject": "Информатика",
        "type": "Лекции",
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
schedule_put()
