from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskForm

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'tasks/dashboard.html')

@login_required(login_url='login')
def create(request):
    context = {'form' : TaskForm}
    if request.method == 'GET':
        return render(request, 'tasks/create.html', context)
    else:
        form = TaskForm(request.POST)
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('dashboard')
        