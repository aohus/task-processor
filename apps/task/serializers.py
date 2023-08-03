import json
from django.db import transaction
from rest_framework import serializers
from task.models import Task, Subtask
from user.models import User


class TaskSerializer(serializers.ModelSerializer):
    def validate_team(self, value: str):
        try:
            value = json.loads(value)
        except Exception as e:
            raise serializers.ValidationError(e)

        if len(value) < 1:
            raise serializers.ValidationError(
                "Team list must have at least one element."
            )
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Team name duplicated")

        invalid_team = set(value) - set(("단비", "다래", "블라블라", "철로", "땅이", "해태", "수피"))
        if invalid_team:
            raise serializers.ValidationError(
                f"Invalid team name '{invalid_team}' included."
            )
        return value

    # def validate(self, attrs):
    #     user: User = self.context["request"].create_user
    #     team: str = attrs["team"]
    #     content: str = attrs["content"]

    @transaction.atomic
    def create(self, validated_data):
        subtask_teams = validated_data.get("team")  # 이거 왜 스트링 아니?
        task = Task.objects.create(**validated_data)
        Subtask.objects.bulk_create(
            [Subtask(task_id=task.id, team=team) for team in subtask_teams]
        )
        return task

    @transaction.atomic
    def update(self, instance, validated_data):
        new_subtask_teams = validated_data.get("team")  # 이거 왜 스트링아니?
        origin_subtask_teams = json.loads(Task.objects.get(id=instance.id).team)
        completed_teams = Subtask.objects.filter(
            task=instance.id, team__in=origin_subtask_teams, is_complete=True
        ).values("team")
        validated_data["team"] = new_subtask_teams.append(completed_teams)

        remove_teams = (
            set(origin_subtask_teams) - set(new_subtask_teams) - set(completed_teams)
        )
        register_teams = set(new_subtask_teams) - set(origin_subtask_teams)

        Subtask.objects.filter(task_id=instance.id, team__in=remove_teams).delete()
        Subtask.objects.bulk_create(
            [Subtask(task_id=instance.id, team=team) for team in register_teams]
        )
        return super().update(validated_data)

    class Meta:
        model = Task
        fields = ["create_user", "team", "title", "content"]


class SubtaskSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        return

    class Meta:
        model = Subtask
        fields = ["team", "is_completed", "completed_date"]
