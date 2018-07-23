from django.urls import path
from .import views

urlpatterns = [
    path('', views.lin, name='lin'),
    path('register', views.Register, name='register')
]