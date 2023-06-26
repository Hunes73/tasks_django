from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from tasks_app.models import Task


class Command(BaseCommand):
    help = 'Initialize the database with initial data'

    def handle(self, *args, **options):
        if User.objects.count() > 0:
            self.stdout.write(self.style.WARNING('Database already initialized.'))
            return
        user1 = User.objects.create_user(username='user1', password='password1')
        user2 = User.objects.create_user(username='user2', password='password2')

        Task.objects.create(name='Zadanie numer 1', description='Opis zadania numer 1', status='Nowe', user=user1)
        Task.objects.create(name='Zadanie numer 2', description='Opis zadania numer 2', status='W toku', user=user1)
        Task.objects.create(name='Zadanie numer 3', description='Opis zadania numer 3', status='Rozwiązane', user=user1)
        Task.objects.create(name='Ćwicznie numer 4', description='Ćwiczenie do wykonania na następne zajęcia', status='Nowe', user=user1)

        Task.objects.create(name='Ćwicznie numer 1', description='Ćwiczenie dla chętnego', status='W toku', user=user2)
        Task.objects.create(name='Ćwicznie o numerze porządkowym 2', description='Ćwiczenie dla nadrabiającego zaległości', status='Rozwiązane', user=user2)

        self.stdout.write(self.style.SUCCESS('Database initialization complete.'))
