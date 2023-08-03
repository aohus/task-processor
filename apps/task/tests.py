import json
import logging

from django.test import TestCase
from django.test import Client
from rest_framework.authtoken.models import Token

from task.views import TaskAPIView, TaskDetailAPIView, SubtaskDetailAPIView
from user.models import User


class TaskAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_0 = User.objects.create(
            id="user000", password="testpassword", username="김윙크", team="단비"
        )
        # self.token_0 = Token.objects.create(user=self.user_0).key
        self.user_1 = User.objects.create(
            id="user001", password="testpassword", username="김크크", team="블라블라"
        )
        # self.token_1 = Token.objects.create(user=self.user_1).key
        self.url = "/task/"

    # def test_get_task_with_unauthenticated(self):
    #     response = self.client.get(
    #         self.url,
    #         header={"Authorization": "Token INVALIDTOKEN"},
    #         content_type="application/json",
    #     )
    #     self.assertEqual(response.status_code, 401)

    # def test_get_task_with_authenticated(self):
    #     response = self.client.get(
    #         self.url,
    #         header={"Authorization": f"Token {self.token_0}"},
    #         content_type="application/json",
    #     )
    #     self.assertEqual(response.status_code, 200)

    def test_create_task_with_unauthenticated(self):
        # with unauthenticated header
        response = self.client.post(
            self.url,
            {
                "create_user": "user000",
                "team": '["철로", "땅이", "해태"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            # header={"Authorization": "Token INVALIDTOKEN"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_create_task_with_invalid_team_field(self):
        # no team name
        response = self.client.post(
            self.url,
            {
                "create_user": "user000",
                "team": "[]",
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            # header={"Authorization": f"Token {self.token_0}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        # invalid team name(블루블루)
        response = self.client.post(
            self.url,
            {
                "create_user": "user000",
                "team": '["철로", "땅이", "블루블루"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            # header={"Authorization": f"Token {self.token_0}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_creat_tasks(self):
        # with unauthenticated header
        response = self.client.post(
            self.url,
            {
                "create_user": "user000",
                "team": '["철로", "땅이", "해태"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            # header={"Authorization": f"Token {self.token_0}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.post(
            self.url,
            {
                "create_user": "user000",
                "team": '["단비", "블라블라", "해태"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            # header={"Authorization": f"Token {self.token_0}"},
            content_type="application/json",
        )
        self.client.post(
            self.url,
            {
                "create_user": "user001",
                "team": '["단비"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            # header={"Authorization": f"Token {self.token_1}"},
            content_type="application/json",
        )
        # user_0(username=김윙크, team=단비)의 tasks 요청 -> 단비팀이 하위 업무로 받은 모든 업무 반환 2개
        response = self.client.get(
            self.url,
            # header={"Authorization": f"Token {self.token_0}"},
            content_type="application/json",
        )
        print(response.data["result_msg"])
        self.assertEqual(response.status_code, 200)

    def test_creat_task_with_no_title(self):
        # title required
        response = self.client.post(
            self.url,
            {
                "create_user": "user001",
                "team": '["철로", "땅이", "해태"]',
                "content": "테스트 업무 내용",
            },
            # header={"Authorization": f"Token {self.token_0}"},
            content_type="application/json",
        )
        self.assertIn("title", response.data["result_msg"].keys())
        self.assertEqual(response.status_code, 400)


class TaskDetailAPIViewTest(TestCase):
    def setUp(self):
        pass


class SubtaskDetailAPIViewTest(TestCase):
    def setUp(self):
        pass
