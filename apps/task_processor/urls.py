from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("task/", include("task.urls")),
    path("user/", include("user.urls")),
    path("admin/", admin.site.urls),
    path("api-token-auth/", obtain_auth_token),
]
