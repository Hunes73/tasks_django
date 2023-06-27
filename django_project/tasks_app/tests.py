from typing import Dict

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer


class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.task1 = Task.objects.create(name='Zadanie #1', description='Opis 1', status='Nowe', user=self.user1)
        self.task2 = Task.objects.create(name='Zadanie #2', description='Opis 2', status='W toku', user=self.user1)
        self.task3 = Task.objects.create(name='Zadanie #3', description='Opis 3', status='Rozwiązane', user=self.user2)

    def test_get_all_tasks(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get('/api/tasks/')
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_task(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(f'/api/tasks/{self.task1.id}/')
        task = Task.objects.get(id=self.task1.id)
        serializer = TaskSerializer(task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_task(self):
        self.client.login(username='user1', password='password1')
        data: dict[str, str] = {
            'name': 'Nowe zadanie',
            'description': 'Nowy opis',
            'status': 'Nowe',
            'username': 'user1',
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.last().name, 'Nowe zadanie')
        self.assertEqual(Task.objects.last().description, 'Nowy opis')
        self.assertEqual(Task.objects.last().status, 'Nowe')
        self.assertEqual(Task.objects.last().user, self.user1)

    def test_update_task(self):
        self.client.login(username='user1', password='password1')
        data = {
            'name': 'Zaktualizowane zadanie',
            'description': 'Zaktualizowany opis',
            'status': 'W toku',
            'username': 'user2',
        }
        response = self.client.put(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, 'Zaktualizowane zadanie')
        self.assertEqual(self.task1.description, 'Zaktualizowany opis')
        self.assertEqual(self.task1.status, 'W toku')
        self.assertEqual(self.task1.user.username, 'user2')

    def test_delete_task(self):
        self.client.login(username='user1', password='password1')
        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_get_my_tasks(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get('/api/tasks/my_tasks/')
        tasks = Task.objects.filter(user=self.user1)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
