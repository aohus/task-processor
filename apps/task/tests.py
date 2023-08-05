import json
import logging

from django.test import TestCase
from django.test import Client
from rest_framework.authtoken.models import Token

from user.models import User
from task.models import Task, Subtask
from task.views import TaskAPIView, TaskDetailAPIView, SubtaskDetailAPIView
from user.views import RegisterAPIView


class ReqObj:
    def __init__(self, data):
        self.data = data


class TaskAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.register = RegisterAPIView()
        cls.user_1_token = Token.objects.create(
            user=User.objects.create(
                id="user001", password="testpassword", username="김단비", team="단비"
            )
        )
        cls.user_2_token = Token.objects.create(
            user=User.objects.create(
                id="user002", password="testpassword", username="김땅이", team="땅이"
            )
        )
        cls.user_3_token = Token.objects.create(
            user=User.objects.create(
                id="user003", password="testpassword", username="김블라", team="블라블라"
            )
        )

        cls.url = "/task/"

    def test_get_task_with_invalid_authenticated(self):
        response = self.client.get(
            self.url,
            content_type="application/json",
        )
        self.assertEqual(response.data["detail"].code, "not_authenticated")
        self.assertEqual(response.status_code, 401)

        response = self.client.get(
            self.url,
            headers={"Authorization": "Token INVALIDTOKEN"},
            content_type="application/json",
        )
        self.assertEqual(response.data["detail"].code, "authentication_failed")
        self.assertEqual(response.status_code, 401)

    def test_get_task_with_authenticated(self):
        response = self.client.get(
            self.url,
            headers={"Authorization": f"Token {self.user_1_token}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_task_with_unauthenticated(self):
        # with unauthenticated header
        response = self.client.post(
            self.url,
            {
                "team": '["철로", "땅이", "해태"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": "Token INVALIDTOKEN"},
            content_type="application/json",
        )
        self.assertEqual(response.data["detail"].code, "authentication_failed")
        self.assertEqual(response.status_code, 401)

    def test_create_task_with_invalid_team_field(self):
        # no team name
        response = self.client.post(
            self.url,
            {
                "team": "[]",
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": f"Token {self.user_2_token}"},
            content_type="application/json",
        )
        self.assertIn("team", response.data["result_msg"].keys())
        self.assertEqual(response.status_code, 400)

        # invalid team name(블루블루)
        response = self.client.post(
            self.url,
            {
                "team": '["철로", "땅이", "블루블루"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": f"Token {self.user_2_token}"},
            content_type="application/json",
        )
        self.assertIn("team", response.data["result_msg"].keys())
        self.assertEqual(response.status_code, 400)

    def test_create_tasks(self):
        response = self.client.post(
            self.url,
            {
                "team": '["철로", "땅이", "해태"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": f"Token {self.user_1_token}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.post(
            self.url,
            {
                "team": '["단비", "해태"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": f"Token {self.user_1_token}"},
            content_type="application/json",
        )
        self.client.post(
            self.url,
            {
                "team": '["단비"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": f"Token {self.user_3_token}"},
            content_type="application/json",
        )
        self.assertEqual(len(Task.objects.all()), 3)

        # user_1(username=김윙크, team=단비)의 tasks 요청 -> 단비팀이 하위 업무로 받은 모든 업무 2개 반환
        # user_2(username=김땅이, team=땅이)의 tasks 요청 -> 땅이팀이 하위 업무로 받은 모든 업무 1개 반환
        # user_3(username=김블라, team=블라블라)의 tasks 요청 -> 블라블라팀이 하위 업무로 받은 모든 업무 0개 반환
        response = self.client.get(
            self.url,
            headers={"Authorization": f"Token {self.user_1_token}"},
            content_type="application/json",
        )
        self.assertEqual(len(response.data["data"]), 2)

        response = self.client.get(
            self.url,
            headers={"Authorization": f"Token {self.user_2_token}"},
            content_type="application/json",
        )
        self.assertEqual(len(response.data["data"]), 1)

        response = self.client.get(
            self.url,
            headers={"Authorization": f"Token {self.user_3_token}"},
            content_type="application/json",
        )
        self.assertEqual(len(response.data["data"]), 0)

    def test_creat_task_with_no_title(self):
        # title required
        response = self.client.post(
            self.url,
            {
                "create_user": "user001",
                "team": '["철로", "땅이", "해태"]',
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": f"Token {self.user_1_token}"},
            content_type="application/json",
        )
        self.assertIn("title", response.data["result_msg"].keys())
        self.assertEqual(response.status_code, 400)


class TaskDetailAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.register = RegisterAPIView()
        cls.user_1_token = Token.objects.create(
            user=User.objects.create(
                id="user001", password="testpassword", username="김단비", team="단비"
            )
        )
        cls.user_2_token = Token.objects.create(
            user=User.objects.create(
                id="user002", password="testpassword", username="김땅이", team="땅이"
            )
        )
        cls.url = "/task/"

        cls.task_1 = cls.client.post(
            cls.url,
            {
                "team": '["철로", "땅이", "해태"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": f"Token {cls.user_1_token}"},
            content_type="application/json",
        ).data["data"]
        cls.ddang_subtask_id = next(
            item["id"] for item in cls.task_1["subtasks"] if item["team"] == "땅이"
        )
        cls.task_id_1 = cls.task_1["id"]

    def test_get_task(self):
        response = self.client.get(
            self.url + str(self.task_id_1),
            headers={"Authorization": f"Token {self.user_1_token}"},
            content_type="application/json",
        )
        self.assertEqual(
            list(response.data["data"].keys()),
            ["id", "create_user", "team", "title", "content", "subtasks"],
        )
        self.assertEqual(response.data["data"]["create_user"], "user001")
        self.assertEqual(response.data["data"]["team"], "['철로', '땅이', '해태']")

    def test_patch_task(self):
        # 땅이팀의 땅이 토큰 2번, subtask 완료처리
        self.client.patch(
            self.url + str(self.task_id_1) + f"/subtask/{self.ddang_subtask_id}",
            headers={"Authorization": f"Token {self.user_2_token}"},
            content_type="application/json",
        )

        response = self.client.patch(
            self.url + str(self.task_id_1),
            {"team": '["철로","다래"]'},
            headers={"Authorization": f"Token {self.user_1_token}"},
            content_type="application/json",
        )
        # 땅이팀은 완료된 task라 삭제되지 않고, 다래만 추가
        self.assertEqual(response.data["data"]["team"], "['철로', '다래', '땅이']")


class SubtaskDetailAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.register = RegisterAPIView()
        cls.user_1_token = Token.objects.create(
            user=User.objects.create(
                id="user001", password="testpassword", username="김단비", team="단비"
            )
        )
        cls.user_2_token = Token.objects.create(
            user=User.objects.create(
                id="user002", password="testpassword", username="김땅이", team="땅이"
            )
        )
        cls.url = "/task/"
        cls.task_1 = cls.client.post(
            cls.url,
            {
                "team": '["단비","땅이"]',
                "title": "테스트 업무",
                "content": "테스트 업무 내용",
            },
            headers={"Authorization": f"Token {cls.user_1_token}"},
            content_type="application/json",
        ).data["data"]

    def test_patch_complete_all_subtasks(self):
        self.client.patch(
            self.url + str(self.task_1["id"]) + f"/subtask/1",
            headers={"Authorization": f"Token {self.user_1_token}"},
            content_type="application/json",
        )
        self.assertEqual(Task.objects.get(id=1).is_complete, False)
        self.client.patch(
            self.url + str(self.task_1["id"]) + f"/subtask/2",
            headers={"Authorization": f"Token {self.user_2_token}"},
            content_type="application/json",
        )
        self.assertEqual(Task.objects.get(id=1).is_complete, True)
