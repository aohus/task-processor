from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from user.models import User


class CustomAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # dispatch는 클라이언트로 들어온 요청이 어떤 요청(get or post)인지 구분해서 처리하도록 분기해주는 녀석
    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        if request.user:
            self.user_id = request.user.id
            self.team = get_object_or_404(User, id=self.user_id).team
            return super(CustomAPIView, self).dispatch(request, *args, **kwargs)
        return None
