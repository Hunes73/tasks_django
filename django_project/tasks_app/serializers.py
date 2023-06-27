from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'username']


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task.history.model
        fields = '__all__'
