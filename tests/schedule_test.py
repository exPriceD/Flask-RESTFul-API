import unittest
import requests
import json
import os


class TestScheduleAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api/v1/"
    maxDiff = None

    def test_get_schedule_by_id(self):
        res = requests.get(self.BASE_URL + "schedule/id/5")
        with open(f'{os.getcwd()}/tests/schedule/get/get_schedule_by_id.json', 'r', encoding="utf8") as f:
            expected_data = json.load(f)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 1 completed")

    def test_get_schedule_by_name(self):
        res = requests.get(self.BASE_URL + "schedule/name/K3140")
        with open(f'{os.getcwd()}/tests/schedule/get/get_schedule_by_name.json', 'r', encoding="utf8") as f:
            expected_data = json.load(f)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 2 completed")

    def test_get_schedule_of_week_number(self):
        res = requests.get(self.BASE_URL + "schedule/name/K3140/2")
        with open(f'{os.getcwd()}/tests/schedule/get/get_schedule_of_week_number.json', 'r', encoding="utf8") as f:
            expected_data = json.load(f)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 3 completed")

    def test_get_schedule_on_day(self):
        res = requests.get(self.BASE_URL + "schedule/name/K3140/2/1")
        with open(f'{os.getcwd()}/tests/schedule/get/get_schedule_on_day.json', 'r', encoding="utf8") as f:
            expected_data = json.load(f)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 4 completed")

    def test_update_group_schedule(self):
        data = {
            "group": "M3117",
            "day": "Friday",
            "even_week": 1,
            "subject": "Информатика",
            "type": "Лекция",
            "time_start": "23:10",
            "time_end": "23:30",
            "teacher_name": "Добриборщ Дмитрий"
        }
        res = requests.put(self.BASE_URL + "schedule/id/2", json=data)
        expected_data = {
            "id": 2,
            "group": "M3117",
            "day": "friday",
            "even_week": True,
            "subject": "Информатика",
            "type": "Лекция",
            "time_start": "23:10",
            "time_end": "23:30",
            "teacher_name": "Добриборщ Дмитрий",
            "room": "2433",
            "address": "Кронверкский пр., д.49, лит.А",
            "zoom_url": "none"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 5 completed")

    def test_post_schedule(self):
        data = {
            "group": "M3117",
            "day": "monday",
            "even_week": False,
            "subject": "Основы программирования",
            "type": "Лекция",
            "time_start": "08:20",
            "time_end": "09:50",
            "teacher_name": "Шиманская Галина Станиславовна",
            "room": "2433",
            "address": "Кронверкский пр., д.49, лит.А",
            "zoom_url": "none"
        }
        res = requests.post(self.BASE_URL + "schedule", json=data)
        expected_data = {
            "group": "M3117",
            "day": "monday",
            "even_week": False,
            "subject": "Основы программирования",
            "type": "Лекция",
            "time_start": "08:20",
            "time_end": "09:50",
            "teacher_name": "Шиманская Галина Станиславовна",
            "room": "2433",
            "address": "Кронверкский пр., д.49, лит.А",
            "zoom_url": "none"
        }
        received_data = res.json()
        try:
            del received_data["id"]
        except KeyError:
            pass
        self.assertEqual(res.status_code, 200)
        self.assertEqual(received_data, expected_data)
        print("Test 6 completed")

    '''def test_del_schedule(self):
        time.sleep(5)
        res = requests.delete(self.BASE_URL + "schedule/id/22")
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.json(), {"status": 202, "message": "Accepted"})
        print("Test 7 completed")'''


if __name__ == "__main__":
    unittest.main(verbosity=2)
