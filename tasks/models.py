from django.db import models
from accounts.models import Account


# Modelo de tareas
class Task(models.Model):

    PRIORITY_CHOICES = [
        (1, 'Lowest'),
        (2, 'Low'),
        (3, 'Normal'),
        (4, 'High'),
        (5, 'Highest'),
    ]

    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    created = models.DateTimeField(auto_now_add=True)
    task_due = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(Account, on_delete= models.CASCADE)

    def __str__(self):
        return self.title