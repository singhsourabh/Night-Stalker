from django.shortcuts import render, redirect
from .forms import userReg
from django.contrib.auth.models import User

def lin(request):
	userForm = userReg()
	return render(request, 'registration/login.html', {'userR':userForm})

def Register(request):
	if request.method == 'POST':
		form1 = userReg(request.POST)
		if form1.is_valid():
			username = form1.cleaned_data['username']
			email = form1.cleaned_data['email']
			password = form1.cleaned_data['password']
			confirm_password = form1.cleaned_data['confirm_password']
			if password == confirm_password:
				User.objects.create_user(username=username, email=email, password=password)
			
	return redirect('lin')
		
