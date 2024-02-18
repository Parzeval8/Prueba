from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

@login_required(login_url='login')
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    context = {'tasks': tasks}
    return render(request, 'tasks/dashboard.html', context)

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

@login_required(login_url='login')
def update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)  # Pasa la instancia de la tarea al formulario
        return render(request, 'tasks/update.html', {'form': form})
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, 'tasks/update.html', {'form': form})
    task = get_object_or_404(Task, id=task_id, user=request.user)
    print(task)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'tasks/update.html', {'form': form, 'task': task})
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print(form)
            # En caso de que el formulario no sea válido, vuelve a renderizar el formulario con los errores
            return render(request, 'tasks/update.html', {'form': form, 'task': task})

@login_required(login_url='login')
def update_done(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        task_id = request.POST.get('task_id')
        done = request.POST.get('done') == 'true'
        date_completed_str = request.POST.get('date_completed')
        task = Task.objects.get(id=task_id)
        task.done = done
        if done and date_completed_str:
            date_completed = parse_datetime(date_completed_str)
            task.date_completed = date_completed
        else:
            task.date_completed = None
        task.save()
        return JsonResponse({'success': True, 'done': done, 'date_completed': str(task.date_completed)})
    return JsonResponse({'success': False})

@login_required(login_url='login')
def delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('dashboard')