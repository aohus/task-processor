from datetime import datetime
import json
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from common.common import SuccessResponse, SuccessResponseWithData, ErrorResponse
from task.models import Task, Subtask
from user.models import User
from task.serializers import TaskSerializer, SubtaskSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class TaskAPIView(APIView):
    """
    GET: 소속 팀이 할당받은 모든 TASK 읽기(권한: 인증된 모든 팀원)
    POST: TASK 생성(권한: 인증된 모든 팀원) -> 생성된 Task ID 반환
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        task_list = Task.objects.filter(Q(team__icontains=request.user.team))
        serializer = TaskSerializer(task_list, many=True)
        return SuccessResponseWithData(data=serializer.data, status=200)

    def post(self, request: Request) -> Response:
        request.data["create_user"] = request.user
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponseWithData(serializer.data, status=201)
        return ErrorResponse(msg=serializer.errors, status=400)


class TaskDetailAPIView(APIView):
    """
    GET: Task ID에 해당하는 Task 읽기(권한: 인증된 모든 팀원)
    PATCH : Task ID에 해당하는 Task 수정(권한: 생성자(create_user))
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, task_id: str) -> Response:
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        return SuccessResponseWithData(serializer.data, status=200)

    def patch(self, request: Request, task_id: str) -> Response:
        # Subtask 상태확인
        task = get_object_or_404(Task, id=task_id)
        if request.user != task.create_user:
            return ErrorResponse(msg="Permission denied.", status=403)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponseWithData(serializer.data, status=200)
        return ErrorResponse(msg=serializer.errors, status=400)


class SubtaskDetailAPIView(APIView):
    """
    PATCH: subtask 완료처리(권한: subtask 할당받은 팀에 소속된 팀원)
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, task_id: str, subtask_id: str) -> Response:
        team = get_object_or_404(User, id=request.user).team
        subtask = get_object_or_404(Subtask, id=subtask_id)
        if team != subtask.team:
            return ErrorResponse(msg="Unauthorized team member", status=403)

        if subtask.is_complete:
            return ErrorResponse(
                msg=f"subtask id: '{subtask.id}' is already completed", status=400
            )
        serializer = SubtaskSerializer(
            subtask,
            data={"is_complete": True, "completed_date": datetime.now()},
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return SuccessResponseWithData(serializer.data, status=201)
        return ErrorResponse(msg=serializer.errors, status=400)
