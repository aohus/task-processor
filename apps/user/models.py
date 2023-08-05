import json
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.CharField(verbose_name="유저 아이디", max_length=24, primary_key=True)
    username = models.CharField(verbose_name="유저 이름", max_length=24)
    password = models.CharField(verbose_name="유저 비밀번호", max_length=128)
    team = models.CharField(verbose_name="유저 소속 팀", max_length=24)
    is_active = models.BooleanField(verbose_name="active", default=True)
    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["username", "team", "password"]

    def save(self, *args, **kwargs):
        self._password = self.password
        if self._password is not None:
            self.set_password(self._password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "user"
        verbose_name = "유저 테이블"
