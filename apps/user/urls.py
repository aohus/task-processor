from django.urls import path
from user.views import RegisterAPIView

urlpatterns = [
    path("register", RegisterAPIView.as_view()),
]
