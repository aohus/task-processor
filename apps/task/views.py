from datetime import datetime
import json
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from common.common import SuccessResponse, SuccessResponseWithData, ErrorResponse
from task.models import Task, Subtask
from user.models import User
from task.serializers import TaskSerializer, SubtaskSerializer


class TaskAPIView(APIView):
    def get(self, request: Request) -> Response:
        # check user team
        # team의 subtask가 속하는 task 반환
        user_id = request.data.get("user_id")
        if user_id is None:
            return ErrorResponse(msg="'user_id' field is required.")

        team = get_object_or_404(User, id=user_id).team
        task_list = Task.objects.filter(Q(team__icontains=team))
        serializer = TaskSerializer(task_list, many=True)
        # TODO: subtask의 처리 상태까지 반환
        return SuccessResponseWithData(data=serializer.data, status=200)

    def post(self, request: Request) -> Response:
        # team length > 1 -> serializer
        # team name in ["", ... 7가지] -> serializer
        # TODO:create task and subtasks ???? -> 이것도 serializer에서????
        # TODO: user_id 따로 받아서 create_user에 넣어주어야 하나?
        # TODO: transaction 처리 잘 되나 테스트
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponseWithData(serializer.data, status=201)
        return ErrorResponse(msg=serializer.errors, status=400)


class TaskDetailAPIView(APIView):
    def get(self, request: Request, task_id: str) -> Response:
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        return SuccessResponseWithData(serializer.data, status=200)

    def patch(self, request: Request, task_id: str) -> Response:
        # Subtask 상태확인
        user_id = request.data.get("user_id")
        if user_id is None:
            return ErrorResponse(msg="'user_id' field is required.", status=400)

        task = get_object_or_404(Task, id=task_id)
        if user_id != task.create_user:
            return ErrorResponse(msg="Unauthorized user", status=403)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponseWithData(serializer.data, status=200)
        return ErrorResponse(msg=serializer.errors, status=400)


class SubtaskDetailAPIView(APIView):
    def patch(self, request: Request, task_id: str, subtask_id: str) -> Response:
        user_id = request.data.get("user_id")
        if user_id is None:
            return ErrorResponse(msg="'user_id' field is required.", status=400)
        team = get_object_or_404(User, id=user_id).team

        try:
            subtask = Subtask.objects.get(id=subtask_id)
        except Subtask.DoesNotExist:
            return ErrorResponse(msg=f"Subtask not found", status=404)

        if team != subtask.team:
            return ErrorResponse(msg="Unauthorized team member", status=403)

        subtask.is_complete = True
        subtask.completed_date = datetime.now()
        serializer = SubtaskSerializer(subtask)
        if serializer.is_valid():
            subtask.save()
            return SuccessResponseWithData(subtask, status=201)
        return ErrorResponse(msg=serializer.errors, status=400)
