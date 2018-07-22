from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import NewUser, Modify
from .models import UserDetail, Sj, Cc, Cf
from .crawler import codechefCrawler, spojCrawler, codeforceCrawler, updater
from dateutil.parser import parse
from datetime import date, datetime, timedelta

def dash(request):
	UserList = UserDetail.objects.all()
	ccList = Cc.objects.all()
	spojList = Sj.objects.all()
	cfList = Cf.objects.all()
	UserForm = NewUser()
	mod = Modify()
	updater.delay()
	context = {'UserList':UserList, 'ccList': ccList, 'spojList': spojList, 'cfList': cfList, 'UserForm':UserForm, 'mod':mod}
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
	return redirect('dashboard')

def dateQ(request):
	Fm = request.POST['From']
	T = request.POST['To']
	Id = request.POST['id']
	From = parse(Fm).date()
	To = parse(T).date()
	Handler = UserDetail.objects.get(name__exact=Id)
	packet = {
		'cc': Cc.objects.filter(handle_id=Handler.pk).filter(date__gte=From).filter(date__lte=To).count(),
		'spoj': Sj.objects.filter(handle_id=Handler.pk).filter(date__gte=From).filter(date__lte=To).count(),
		'cf': Cf.objects.filter(handle_id=Handler.pk).filter(date__gte=From).filter(date__lte=To).count(),
	}
	print(Cc.objects.filter(handle_id=Handler.pk).filter(date__gte=From).filter(date__lte=To).count())
	return JsonResponse(packet)

def modify(request, userid):
	nCc = request.POST['mcodechef']
	nSj = request.POST['mspoj']
	nCf = request.POST['mcodeforce'] 
	users = UserDetail.objects.get(pk=userid)
	ucc = users.codechef
	usj = users.spoj
	ucf = users.codeforce
	if nCc:
		Cc.objects.filter(handle_id__exact=userid).delete()
		ucc = nCc
	if nSj:
		Sj.objects.filter(handle_id__exact=userid).delete()
		usj = nSj
	if nCf:
		Cf.objects.filter(handle_id__exact=userid).delete()
		ucf = nCf
	users.last_sync = date.today() -timedelta(days=1)
	users.codechef = ucc
	users.spoj = usj
	users.codeforce = ucf
	users.save()
	return redirect('dashboard')
	
def remove(request):
	opt = request.POST.getlist('checks[]')
	for item in opt:
		UserDetail.objects.get(pk=int(item)).delete()
	return redirect('dashboard')