from django.shortcuts import render

def dash(request):
	return render(request, 'dashboard/dashboard.html')