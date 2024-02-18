from django.db import models
from accounts.models import Account

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(default=3)
    created = models.DateTimeField(auto_now_add=True)
    task_due = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(Account, on_delete= models.CASCADE)