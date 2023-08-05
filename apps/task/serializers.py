import json
from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from task.models import Task, Subtask
from user.models import User


class TaskSerializer(serializers.ModelSerializer):
    subtasks = serializers.SerializerMethodField("get_subtasks")

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

    def get_subtasks(self, instance):
        subtask_teams = Subtask.objects.filter(task=instance).values()
        return list(subtask_teams)

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
        old_subtask_teams = eval(Task.objects.get(id=instance.id).team)
        completed_teams = Subtask.objects.filter(
            task=instance.id, team__in=old_subtask_teams, is_complete=True
        ).values_list("team", flat=True)

        validated_data["team"] = new_subtask_teams + list(completed_teams)
        teams_to_remove = (
            set(old_subtask_teams) - set(new_subtask_teams) - set(list(completed_teams))
        )

        teams_to_add = set(new_subtask_teams) - set(old_subtask_teams)

        Subtask.objects.filter(task_id=instance.id, team__in=teams_to_remove).delete()
        Subtask.objects.bulk_create(
            [Subtask(task_id=instance.id, team=team) for team in teams_to_add]
        )
        return super().update(instance, validated_data)

    class Meta:
        model = Task
        fields = ["id", "create_user", "team", "title", "content", "subtasks"]


class SubtaskSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # TODO: Task 완료 여부 확인하고 완료 처리
        instance.is_complete = validated_data.get("is_complete", instance.is_complete)
        instance.completed_date = validated_data.get(
            "completed_date", instance.completed_date
        )
        instance.save()
        subtasks_incomplete = Subtask.objects.filter(task_id=instance.task_id).exclude(
            is_complete=True
        )
        if not subtasks_incomplete:
            task = Task.objects.get(id=instance.task_id)
            task.is_complete = True
            task.completed_date = datetime.now()
            task.save()
        return instance

    class Meta:
        model = Subtask
        fields = ["id", "team", "is_complete", "completed_date"]
