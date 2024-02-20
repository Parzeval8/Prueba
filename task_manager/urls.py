from django.contrib import admin
from django.urls import path, include
from . import views

#Direccionamiento principal
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),

]