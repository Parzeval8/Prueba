from django.db import models
from accounts.models import Account

# Create your models here.
class Task(models.Model):

    PRIORITY_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
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