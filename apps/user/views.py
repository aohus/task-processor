from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from common.common import SuccessResponse, SuccessResponseWithData, ErrorResponse
from user.models import User
from user.serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return SuccessResponseWithData({"Token": token.key}, status=201)
        return ErrorResponse(msg=serializer.errors, status=400)
