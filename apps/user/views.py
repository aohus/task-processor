from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token

from common.common import SuccessResponse, SuccessResponseWithData, ErrorResponse
from user.models import User
from user.serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponseWithData(serializer.data, status=201)
        return ErrorResponse(msg=serializer.errors, status=400)


class LoginAPIView(APIView):
    def post(self, request):
        pass
        # user = User.objects.get(username=data["id"])
        # token, created = Token.objects.get_or_create(user=user)
        # token.key
        # id = request.data.get("id", None)
        # password = request.data.get("password", None)
        # is_valid_password = check_password('mypassword', password)
