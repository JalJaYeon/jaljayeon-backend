from apps.user.models import User
from rest_framework.test import APITestCase


class TestUserRegistration(APITestCase):
    ENDPOINT = "/api/users/register"

    def test_user_registration_should_success(self):
        response = self.client.post(
            self.ENDPOINT, {
                "name": "홍길동",
                "username": "test_user",
                "password": "thePAS123!Q",
                "weight_kg": 71,
                "average_sleep_time": "06:30",
                "bedtime_starts_at": "00:10",
            })
        self.assertEqual(201, response.status_code)
        self.assertEqual("홍길동", response.data["name"])
        self.assertEqual("test_user", response.data["username"])
        self.assertEqual(71, response.data["weight_kg"])
        self.assertEqual("06:30", response.data["average_sleep_time"])
        self.assertEqual("00:10", response.data["bedtime_starts_at"])

    def test_wrong_weight_kg_should_fail(self):
        response = self.client.post(
            self.ENDPOINT, {
                "name": "홍길동",
                "username": "test_user",
                "password": "thePAS123!Q",
                "weight_kg": -1,
                "average_sleep_time": "06:30",
                "bedtime_starts_at": "00:10",
            })
        self.assertEqual(400, response.status_code)

    def test_wrong_average_sleep_time_format_should_fail(self):
        response = self.client.post(
            self.ENDPOINT, {
                "name": "홍길동",
                "username": "test_user",
                "password": "thePAS123!Q",
                "weight_kg": 71,
                "average_sleep_time": "1",
                "bedtime_starts_at": "23:30",
            })
        self.assertEqual(400, response.status_code)

    def test_wrong_average_sleep_time_format_should_fail(self):
        response = self.client.post(
            self.ENDPOINT, {
                "name": "홍길동",
                "username": "test_user",
                "password": "thePAS123!Q",
                "weight_kg": 71,
                "average_sleep_time": "06:30",
                "bedtime_starts_at": "asdf",
            })
        self.assertEqual(400, response.status_code)


class TestUserIssuingToken(APITestCase):
    def test_issuing_token_should_success(self):
        response = self.client.post(
            "/api/users/register", {
                "name": "홍길동",
                "username": "test_user",
                "password": "thePAS123!Q",
                "weight_kg": 71,
                "average_sleep_time": "06:30",
                "bedtime_starts_at": "00:10",
            })

        response = self.client.post(
            '/api/token',
            {
                "username": "test_user",
                "password": "thePAS123!Q",
            },
        )
        self.assertEqual(200, response.status_code)