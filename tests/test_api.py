import unittest
import requests
import json


class TestAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api/v1/"

    def test_get_full_schedule(self):
        res = requests.get(self.BASE_URL + "schedule")
        with open('get_full_schedule.json', 'r', encoding="utf8") as f:
            get_full_schedule_data = json.load(f)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), get_full_schedule_data)
        print("Test 1 completed")

    def test_get_schedule_by_id(self):
        pass


if __name__ == "__main__":
    tester = TestAPI()
    tester.test_get_full_schedule()
