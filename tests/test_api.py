import unittest
import requests
import json
import os


class TestAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api/v1/"

    def test_get_full_schedule(self):
        res = requests.get(self.BASE_URL + "schedule")
        with open(f'{os.getcwd()}/schedule/get_schedule.json', 'r', encoding="utf8") as f:
            get_full_schedule_data = json.load(f)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), get_full_schedule_data)
        print("Test 1 completed")

    def test_get_schedule_by_id(self):
        res = requests.get(self.BASE_URL + "schedule/id/5")
        with open('schedule/get_schedule_by_id.json', 'r', encoding="utf8") as f:
            get_schedule_by_id_data = json.load(f)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), get_schedule_by_id_data)
        print("Test 2 completed")

    def test_get_schedule_by_name(self):
        res = requests.get(self.BASE_URL + "schedule/name/K3140")
        with open('schedule/get_schedule_by_name.json', 'r', encoding="utf8") as f:
            get_schedule_by_name_data = json.load(f)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), get_schedule_by_name_data)
        print("Test 3 completed")


if __name__ == "__main__":
    tester = TestAPI()
    tester.test_get_full_schedule()
    tester.test_get_schedule_by_id()
    tester.test_get_schedule_by_name()
