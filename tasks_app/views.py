from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer, TaskHistorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user_id', 'status']
    search_fields = ['name', 'description']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        return queryset

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Invalid username.')

        request_data = request.data.copy()
        request_data.pop('username', None)

        task = Task.objects.create(user=user, **request_data)
        serializer = TaskSerializer(task)
        response_data = serializer.data
        response_data['username'] = user.username

        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request_data = request.data.copy()
        request_data.pop('id', None)

        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        response_data = TaskSerializer(task).data
        response_data['username'] = task.user.username

        return Response(response_data)

    @action(detail=True, methods=['get'])
    def history(self, request, **kwargs):
        instance = self.get_object()
        history = instance.history.all()
        serializer = TaskHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all_history(self, request, **kwargs):
        queryset = Task.history.all()
        queryset = self.filter_queryset(queryset)
        serializer = TaskHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='history-as-of')
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='datetime',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
                description='Datetime to retrieve the model as of (YYYY-MM-DDTHH:MM:SS)',
            )
        ]
    )
    def history_as_of(self, request, **kwargs):
        instance = self.get_object()
        datetime_str = request.query_params.get('datetime')

        try:
            datetime_obj = datetime.fromisoformat(datetime_str)
        except ValueError:
            raise ValidationError('Invalid datetime format. Expected format: YYYY-MM-DDTHH:MM:SS')

        history = instance.history.filter(history_date__lte=datetime_obj).latest_of_each()
        serializer = TaskHistorySerializer(history, many=True)

        return Response(serializer.data)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/api/tasks/my_tasks')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


class LogoutView(APIView):
    @staticmethod
    def post(request):
        logout(request)
        return Response({"detail": "Logged out successfully"})
