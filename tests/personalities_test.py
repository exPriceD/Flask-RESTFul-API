import unittest
import requests


class TestPersonalitiesAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api/v1/"
    maxDiff = None

    def test_get_person_by_id(self):
        res = requests.get(self.BASE_URL + "personalities/id/2")
        expected_data = {
            "data": {
                "2": {
                    "id": 2,
                    "fio": "Лукичева Алиса Юрьевна",
                    "gender": "female",
                    "phone": "+79114223909",
                    "email": "479573@edu.itmo.ru",
                    "work": None,
                    "education": None
                }
            }
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 1 completed")

    def test_get_person_by_email(self):
        res = requests.get(self.BASE_URL + "personalities/email/479573@edu.itmo.ru")
        expected_data = {
            "data": {
                "2": {
                    "id": 2,
                    "fio": "Лукичева Алиса Юрьевна",
                    "gender": "female",
                    "phone": "+79114223909",
                    "email": "479573@edu.itmo.ru",
                    "work": None,
                    "education": None
                }
            }
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 2 completed")

    def test_get_person_by_phone(self):
        res = requests.get(self.BASE_URL + "personalities/phone/+79114223909")
        expected_data = {
            "data": {
                "2": {
                    "id": 2,
                    "fio": "Лукичева Алиса Юрьевна",
                    "gender": "female",
                    "phone": "+79114223909",
                    "email": "479573@edu.itmo.ru",
                    "work": None,
                    "education": None
                }
            }
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 3 completed")

    def test_post_person(self):
        data = {
            "fio": "Бобиков Аднрей Александрович",
            "gender": "male",
            "phone": "+79123456789",
            "email": "123456789@edu.itmo.ru",
            "work": "ITMO",
            "education": "ITMO"
        }
        res = requests.post(self.BASE_URL + "personalities", json=data)
        expected_data = {
            "id": 5,
            "fio": "Бобиков Аднрей Александрович",
            "gender": "male",
            "phone": "+79123456789",
            "email": "123456789@edu.itmo.ru",
            "work": "ITMO",
            "education": "ITMO"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 4 completed")

    def test_update_person_by_id(self):
        data = {
            "fio": "Бобиков Максим Александрович",
            "email": "max@edu.itmo.ru",
            "work": "ITMO",
            "education": "SPBGU"
        }
        res = requests.put(self.BASE_URL + "personalities/id/4", json=data)
        expected_data = {
            "id": 4,
            "fio": "Бобиков Максим Александрович",
            "gender": "male",
            "phone": "+79531234567",
            "email": "max@edu.itmo.ru",
            "work": "ITMO",
            "education": "SPBGU"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 5 completed")

    '''def test_delete_person(self):
        res = requests.delete(self.BASE_URL + "personalities/id/3")
        expected_data = {"status": 202, "message": "Accepted"}
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.json(), expected_data)
        print("Test 6 completed")'''


if __name__ == "__main__":
    unittest.main(verbosity=2)