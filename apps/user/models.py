import json
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    id = models.CharField(verbose_name="유저 아이디", max_length=24, primary_key=True)
    username = models.CharField(verbose_name="유저 이름", max_length=24)
    password = models.CharField(verbose_name="유저 비밀번호", max_length=128)
    team = models.CharField(verbose_name="유저 소속 팀", max_length=24)
    USERNAME_FIELD = "username"

    class Meta:
        db_table = "user"
        verbose_name = "유저 테이블"
