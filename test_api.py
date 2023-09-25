import unittest
import requests
import json


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api/v1/"
    SCHEDULE_URL = "http://127.0.0.1:5000/api/v1/schedule"
    GROUPS_URL = "http://127.0.0.1:5000/api/v1/groups"
    PERSONALITIES_URL = "http://127.0.0.1:5000/api/v1/personalities"


    def test_get_full_schedule(self):
        resp = requests.get(self.SCHEDULE_URL)
        with open('tests/get_full_schedule.json', 'r') as f:
            get_full_schedule_data = json.load(f)
        self.assertEquals(resp.status_code, 200)
        self.assertDictEquals(resp.json(), get_full_schedule_data)
        print("Test 1 completed")


if __name__ == "__main__":
    tester = TestAPI()
    tester.test_get_full_schedule()
