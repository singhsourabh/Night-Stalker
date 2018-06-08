from django.shortcuts import render

def lin(request):
	return render(request, 'registration/login.html')
