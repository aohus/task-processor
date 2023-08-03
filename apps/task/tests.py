# from django.test import TestCase
# from django.test import Client
# from rest_framework.authtoken.models import Token

# # from django.contrib.auth import get_user_model
# from task.views import TaskAPIView, TaskDetailAPIView, SubtaskDetailAPIView

# from user.models import User
# import json
# import logging
# import statistics


# class TaskAPIViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user_0 = User.objects.create(
#             id="user000", password="testpassword", username="김윙크", team="단비"
#         )
#         self.token_0 = Token.objects.create(user=self.user_0).key
#         self.user_1 = User.objects.create(
#             id="user001", password="testpassword", username="김크크", team="블라블라"
#         )
#         self.token_1 = Token.objects.create(user=self.user_1).key

#         self.TEST_HEADER_0 = {"Authorization": "Token INVALIDTOKEN"}  # unauthenticated
#         self.TEST_HEADER_1 = {"Authorization": f"Token {self.token_0}"}  # authenticated
#         self.TEST_HEADER_1 = {"Authorization": f"Token {self.token_1}"}  # authenticated
#         self.TEST_POST_REQUEST_TRUE_0 = {
#             "create_user": "user000",
#             "team": '["단비", "블라블라"]',
#             "title": "테스트 업무1",
#             "content": "테스트 업무1 내용",
#         }
#         self.TEST_POST_REQUEST_TRUE_1 = {
#             "create_user": "user001",
#             "team": '["철로", "땅이", "해태"]',
#             "title": "테스트 업무2",
#             "test_content": "테스트 업무2 내용",
#         }
#         self.TEST_POST_REQUEST_FALSE_0 = {  # with unauthenticated header
#             "create_user": "user001",
#             "team": '["철로", "땅이", "해태"]',
#             "title": "테스트 업무3",
#             "content": "테스트 업무3 내용",
#         }
#         self.TEST_POST_REQUEST_FALSE_1 = {  # title required
#             "create_user": "user001",
#             "team": '["철로", "땅이", "해태"]',
#             "title": "테스트 업무3",
#             "content": "테스트 업무3 내용",
#         }
#         self.TEST_POST_REQUEST_FALSE_2 = {  # invalid team name(블루블루)
#             "create_user": "user001",
#             "team": '["철로", "땅이", "블루블루"]',
#             "title": "테스트 업무3",
#             "content": "테스트 업무3 내용",
#         }
#         self.TEST_POST_REQUEST_FALSE_3 = {  # no team
#             "create_user": "user001",
#             "team": "[]",
#             "title": "테스트 업무3",
#             "content": "테스트 업무3 내용",
#         }
#         self.url = "/task/"

#     def test_get_with_unauthenticated(self):
#         response = self.client.get(
#             self.url,
#             header=self.TEST_HEADER_0,
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, 401)

#     def test_get_with_authenticated(self):
#         response = self.client.get(
#             self.url,
#             header=self.TEST_HEADER_1,
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_post_with_unauthenticated(self):
#         response = self.client.post(
#             self.url,
#             self.TEST_POST_REQUEST_FALSE_0,
#             header=self.TEST_HEADER_0,
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, 401)


# class TaskDetailAPIViewTest(TestCase):
#     def setUp(self):
#         pass


# class SubtaskDetailAPIViewTest(TestCase):
#     def setUp(self):
#         pass
