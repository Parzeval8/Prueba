from django.forms import ModelForm, DateTimeInput, Textarea
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'task_due']
        widgets = {
            'task_due': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'description': Textarea(attrs={'class': 'form-control'})
        }