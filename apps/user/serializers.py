import json
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    def validate_team(self, value: str):
        if value not in ["단비", "다래", "블라블라", "철로", "땅이", "해태", "수피"]:
            raise serializers.ValidationError(f"Invalid team name '{value}'")
        return value

    class Meta:
        model = User
        fields = "__all__"
