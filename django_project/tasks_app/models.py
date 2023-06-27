from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User


class Task(models.Model):
    objects = models.Manager()
    STATUS_CHOICES = [
        ('Nowy', 'Nowy'),
        ('W toku', 'W toku'),
        ('Rozwiązany', 'Rozwiązany'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Nowy')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
