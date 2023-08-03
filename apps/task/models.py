import json
from django.db import models
from user.models import User


class Task(models.Model):
    id = models.AutoField(verbose_name="업무 id", primary_key=True)
    create_user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="업무 생성한 user_id"
    )
    team = models.TextField(verbose_name="하위업무 설정한 team list")
    title = models.TextField(verbose_name="업무 제목")
    content = models.TextField(verbose_name="업무 내용")
    is_complete = models.BooleanField(verbose_name="업무 완료 여부", default=False)
    completed_date = models.DateTimeField(verbose_name="업무 완료 시간", null=True)
    created_at = models.DateTimeField(verbose_name="업무 생성시간", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="업무 수정시간", auto_now=True)

    class Meta:
        db_table = "task"
        verbose_name = "업무 테이블"


class Subtask(models.Model):
    id = models.AutoField(verbose_name="하위 업무 id", primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="task id")
    team = models.TextField(verbose_name="하위업무 담당 team")
    is_complete = models.BooleanField(verbose_name="하위 업무 완료 여부", default=False)
    completed_date = models.DateTimeField(verbose_name="업무 완료 시간", null=True)
    created_at = models.DateTimeField(verbose_name="업무 생성시간", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="업무 수정시간", auto_now=True)
