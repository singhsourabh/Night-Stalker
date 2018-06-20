from django.urls import path
from .import views

urlpatterns = [
    path('dashboard', views.dash, name='dashboard'),
    path('add', views.add, name='add')
]