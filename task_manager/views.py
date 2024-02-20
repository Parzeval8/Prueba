from django.shortcuts import render

#Vista para reenderizar el home
def home(request):
    return render(request, 'home.html')