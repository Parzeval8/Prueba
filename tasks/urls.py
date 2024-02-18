from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create, name='create'),
    path('update/<int:task_id>/', views.update, name='update'),
    path('update_done/', views.update_done, name='update_done'),
]