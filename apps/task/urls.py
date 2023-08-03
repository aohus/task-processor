from django.urls import path
from task.views import TaskAPIView, TaskDetailAPIView, SubtaskDetailAPIView

urlpatterns = [
    path("", TaskAPIView.as_view()),
    path("<str:task_id>", TaskDetailAPIView.as_view()),
    path("<str:task_id>/subtask/<str:subtask_id>", SubtaskDetailAPIView.as_view()),
]
