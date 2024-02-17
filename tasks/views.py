from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'tasks/home.html')

def signup(request):
    context = {'form' : UserCreationForm}
    return render(request, 'accounts/signup.html', context)