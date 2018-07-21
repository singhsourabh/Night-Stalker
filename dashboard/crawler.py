from celery import shared_task
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from .models import User, Sj, Cc, Cf
from dateutil.parser import parse
from datetime import date, datetime
from django.db.models import F

@shared_task
def getDate(url):
	uClient = uReq('http://www.spoj.com' + url)
	html = uClient.read()
	uClient.close()
	page = soup(html, 'lxml')
	date = page.find('td', class_='status_sm')
	return date.span.text

@shared_task
def spojCrawler(username):
    url = 'http://www.spoj.com/users/'+username
    handler = User.objects.get(spoj=username) 
    uClient = uReq(url)
    html = uClient.read()
    uClient.close()
    page = soup(html, 'lxml')
    content = page.find('table', class_='table table-condensed')
    entry = 0
    if content:
        content = content.findAll('td')
        for x in content:
            if(x.a.text == ''):
                pass
            else:
                entry = entry +1
                newEntry = Sj(handle=handler, problem=x.a.text.strip(), date=parse(getDate(x.a["href"])).date())
                newEntry.save()
    handler.last_sync = date.today().strftime('%Y-%m-%d')
    handler.totalCC = F('totalCC')
    handler.totalSJ = F('totalSJ')+entry
    handler.totalCF = F('totalCF')
    handler.save()
    print('success spoj', entry)
    
@shared_task
def ccDate(url):
	page  = requests.get('https://www.codechef.com'+url)
	souper=soup(page.content, 'lxml')
	table = souper.find('table', class_='dataTable').tbody.tr
	table = table.findAll('td')
	return table[1].text

@shared_task
def codechefCrawler(username):
    
    page  = requests.get('https://www.codechef.com/users/'+username)
    souper = soup(page.content, 'lxml')
    content = souper.find('section', class_='rating-data-section problems-solved')
    entry = 0
    handler = None
    if content:
        handler = User.objects.get(codechef=username)
        content = content.article
        content = content.findAll('a')
        for x in content[::-1]:
            entry = entry +1
            Date = ccDate(x['href'])
            handler.totalCC = F('totalCC')+1
            if 'ago' in Date:
                newEntry = Cc(handle=handler, problem=x.text, date=date.today())
                newEntry.save()
            else:
                dt = Date
                dt = dt[:15] + '20' + dt[15:]
                dt = dt[9:]
                newEntry = Cc(handle=handler, problem=x.text, date=datetime.strptime( dt, "%d/%m/%Y" ).date())
                #print(datetime.strptime( dt, "%d/%m/%Y" ).month)
                newEntry.save()
            
    handler.last_sync = date.today().strftime('%Y-%m-%d')
    handler.totalCC = F('totalCC')+entry
    handler.totalSJ = F('totalSJ')
    handler.totalCF = F('totalCF')
    handler.save()
    print('success cc', entry)

@shared_task
def data(url, index, username):
    handler = User.objects.get(codeforce__exact=username)
    entry = 0
    for x in range(1,index+1):
        uClient = uReq(url+'/page/'+str(x))
        html = uClient.read()
        uClient.close()
        page = soup(html, 'lxml')
        content = page.find('table', class_='status-frame-datatable')
        content = content.findAll('tr')
        
        content.pop(0)
        for x in content:
            info = x.findAll('td', class_='status-small')
            entry = entry +1
            newEntry = Cf(handle=handler, problem=info[1].a.text.strip(), date=parse(info[0].text.strip()).date())
            newEntry.save()
    handler.last_sync = date.today().strftime('%Y-%m-%d')
    handler.totalCC = F('totalCC')
    handler.totalSJ = F('totalSJ')
    handler.totalCF = F('totalCF')+entry -handler.totalCF
    handler.save()
    print('success cf', entry)

@shared_task
def codeforceCrawler(username):
    url = 'https://codeforces.com/submissions/' + username
    uClient = uReq(url)
    html = uClient.read()
    uClient.close()
    page = soup(html, 'lxml')
    maxIndex = [int(x.text) for x in page.findAll('span', class_='page-index')]
    maxId = 1
    if maxIndex:
        maxId = max(maxIndex)
    if maxId < 129:
        data(url, maxId, username)

@shared_task
def updater():
    for users in User.objects.all():
        if users.last_sync != date.today() and users.last_sync:

            #codechef
            if users.codechef:
                page  = requests.get('https://www.codechef.com/users/'+users.codechef)
                souper = soup(page.content, 'lxml')
                content = souper.find('section', class_='rating-data-section problems-solved')
                entry = users.totalCC
                if content:
                    content = content.article
                    content = content.findAll('a')
                for x in content[::-1]:
                    if not Cc.objects.filter(handle_id__exact=users.pk).filter(problem__exact=x.text):
                        entry = entry +1
                        Date = ccDate(x['href'])
                        users.totalCC = F('totalCC')+1
                        if 'ago' in Date:
                            newEntry = Cc(handle=users, problem=x.text, date=date.today())
                            newEntry.save()
                        else:
                            dt = Date
                            dt = dt[:15] + '20' + dt[15:]
                            dt = dt[9:]
                            newEntry = Cc(handle=users, problem=x.text, date=datetime.strptime( dt, "%d/%m/%Y" ).date())
                            #print(datetime.strptime( dt, "%d/%m/%Y" ).month)
                            newEntry.save()
                    else:
                        break
                users.last_sync = date.today().strftime('%Y-%m-%d')
                users.totalCC = F('totalCC')+entry -users.totalCC
                users.totalSJ = F('totalSJ')
                users.totalCF = F('totalCF')
                users.save()
                print('success update cc', entry)

                #spoj
            if users.spoj:
                url = 'http://www.spoj.com/users/'+ users.spoj
                uClient = uReq(url)
                html = uClient.read()
                uClient.close()
                page = soup(html, 'lxml')
                content = page.find('table', class_='table table-condensed')
                entry = users.totalSJ
                if content:
                    content = content.findAll('td')
                    for x in content:
                        if not Sj.objects.filter(handle_id__exact=users.pk).filter(problem__exact=x.a.text.strip()):
                            if(x.a.text == ''):
                                pass
                            else:
                                entry = entry +1
                                newEntry = Sj(handle=users, problem=x.a.text.strip(), date=parse(getDate(x.a["href"])).date())
                                newEntry.save()
                users.last_sync = date.today().strftime('%Y-%m-%d')
                users.totalCC = F('totalCC')
                users.totalSJ = F('totalSJ')+entry -users.totalSJ
                users.totalCF = F('totalCF')
                users.save()
                print('success update spoj', entry)

            if users.codeforce:
                #codeforces
                cfDel = Cf.objects.filter(handle_id__exact=users.pk)
                cfDel.delete()
                codeforceCrawler(users.codeforce)
                print('success update cf')