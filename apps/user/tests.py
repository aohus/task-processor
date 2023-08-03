from django.test import TestCase
from django.test import Client
import json
import logging
import statistics


class RegisterAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/user/register"

    def test_register_and_duplicate(self):
        # 성공
        response = self.client.post(
            self.url,
            {
                "id": "testid",
                "password": "testpassword",
                "username": "testname",
                "team": "단비",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        # duplicated id
        response = self.client.post(
            self.url,
            {
                "id": "testid",
                "password": "testpassword",
                "username": "testname",
                "team": "단비",
            },
            content_type="application/json",
        )
        self.assertIn("id", response.data["result_msg"].keys())
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_team(self):
        # invalid team name
        response = self.client.post(
            self.url,
            {
                "id": "testid",
                "password": "testpassword",
                "username": "testname",
                "team": "없는팀",
            },
            content_type="application/json",
        )
        self.assertIn("team", response.data["result_msg"].keys())
        self.assertEqual(response.status_code, 400)

    def test_register_no_username(self):
        # no username field
        response = self.client.post(
            self.url,
            {"id": "testidnew", "password": "testpassword", "team": "블라블라"},
            content_type="application/json",
        )
        self.assertIn("username", response.data["result_msg"].keys())
        self.assertEqual(response.status_code, 400)

    def test_register_no_body(self):
        # no body field
        response = self.client.post(
            self.url,
            content_type="application/json",
        )
        self.assertEqual(
            ["id", "username", "password", "team"],
            list(response.data["result_msg"].keys()),
        )
        self.assertEqual(response.status_code, 400)
