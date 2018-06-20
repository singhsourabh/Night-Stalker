from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewUser
from .models import User

def dash(request):
	UserList = User.objects.all()
	UserForm = NewUser()
	context = {'UserList':UserList, 'UserForm':UserForm}
	return render(request, 'dashboard/dashboard.html', context)

def add(request):
	nwUser = NewUser(request.POST)
	if nwUser.is_valid():
		nwUser.save()
	return HttpResponse('')