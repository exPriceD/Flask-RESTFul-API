import unittest
import requests
import json
import os

class TestGroupsAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api/v1/"
    maxDiff = None

    def test_get_group_by_id(self):
        res = requests.get(self.BASE_URL + "groups/id/3")
        expected_data = {
            "data": {
                "M3117": {
                    "id": 3,
                    "name": "M3117",
                    "faculty": "FITIP",
                    "direction": "Software Engineering",
                    "people_count": 22
                }
            }
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 1 completed")

    def test_get_group_by_name(self):
        res = requests.get(self.BASE_URL + "groups/name/K3140")
        expected_data ={
            "data": {
                "K3140": {
                    "id": 1,
                    "name": "K3140",
                    "faculty": "ICT",
                    "direction": "Mobile developing",
                    "people_count": 50
                }
            }
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 2 completed")

    def test_post_group(self):
        data = {
            "name": "K3144",
            "faculty": "ICT",
            "direction": "Mobile developing",
            "people_count": 30
        }
        res = requests.post(self.BASE_URL + "groups", json=data)
        expected_data = {
            "name": "K3144",
            "faculty": "ICT",
            "direction": "Mobile developing",
            "people_count": 30
        }
        received_data = res.json()
        try:
            del received_data["id"]
        except KeyError:
            pass
        self.assertEqual(res.status_code, 200)
        self.assertEqual(received_data, expected_data)
        print("Test 3 completed")

    def test_update_group_by_id(self):
        data = {
            "name": "K3138",
            "people_count": 50
        }
        res = requests.put(self.BASE_URL + "groups/id/2", json=data)
        expected_data = {
            "id": 2,
            "name": "K3138",
            "faculty": "ICT",
            "direction": "Mobile developing",
            "people_count": 50
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_data)
        print("Test 4 completed")

    '''def test_delete_group(self):
        res = requests.delete(self.BASE_URL + "groups/id/4")
        expected_data = {"status": 202, "message": "Accepted"}
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.json(), expected_data)
        print("Test 5 completed")'''


if __name__ == "__main__":
    unittest.main(verbosity=2)