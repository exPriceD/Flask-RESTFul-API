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


personalities_post()
