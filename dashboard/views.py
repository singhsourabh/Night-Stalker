from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import NewUser
from .models import User, Sj, Cc, Cf
from .crawler import codechefCrawler, spojCrawler, codeforceCrawler
from dateutil.parser import parse
from datetime import date, datetime

def dash(request):
	UserList = User.objects.all()
	ccList = Cc.objects.all()
	spojList = Sj.objects.all()
	cfList = Cf.objects.all()
	UserForm = NewUser()
	context = {'UserList':UserList, 'ccList': ccList, 'spojList': spojList, 'cfList': cfList, 'UserForm':UserForm}
	return render(request, 'dashboard/dashboard.html', context)

def add(request):
	nwUser = NewUser(request.POST)
	if nwUser.is_valid():
		nwUser.save()
		ccName = request.POST['codechef']
		spojName = request.POST['spoj']
		cfName = request.POST['codeforce']
		if ccName:
			codechefCrawler.delay(ccName)
		if spojName:
			spojCrawler.delay(spojName)
		if cfName:
			codeforceCrawler.delay(cfName)
		print('success')
	return HttpResponse('')

def dateQ(request):
	From = request.POST['From']
	To = request.POST['To']
	Id = request.POST['id']
	Handler = User.objects.get(name__exact=Id)
	packet = {
		'cc': Cc.objects.filter(handle_id=Handler.pk).filter(date__lte=To).filter(date__gte=From).count(),
		'spoj': Sj.objects.filter(handle_id=Handler.pk).filter(date__lte=To).filter(date__gte=From).count(),
		'cf': Cf.objects.filter(handle_id=Handler.pk).filter(date__lte=To).filter(date__gte=From).count(),
	}
	return JsonResponse(packet)

# def dateCc(request):
# 	username = request.GET.get('id', None)
# 	packet = {
# 		'cc': Cc.objects.filter(userid__exact=username).count()
# 	}
# 	return JsonResponse(packet)