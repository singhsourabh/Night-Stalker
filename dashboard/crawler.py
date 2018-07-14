from celery import shared_task
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from .models import User, Sj, Cc, Cf
from dateutil.parser import parse
from datetime import date, datetime

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
                newEntry = Sj(handle=handler, date=parse(getDate(x.a["href"])).date())
                newEntry.save()
    handler.last_sync = date.today().strftime('%Y-%m-%d')
    handler.totalCC = Cc.objects.filter(handle_id=handler.pk).count()
    handler.totalSJ = Sj.objects.filter(handle_id=handler.pk).count()
    handler.totalCF = Cf.objects.filter(handle_id=handler.pk).count()
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
    handler = User.objects.get(codechef=username)
    page  = requests.get('https://www.codechef.com/users/'+username)
    souper = soup(page.content, 'lxml')
    content = souper.find('section', class_='rating-data-section problems-solved')
    entry = 0
    if content:
        content = content.article
        content = content.findAll('a')
        for x in content[::-1]:
            entry = entry +1
            Date = ccDate(x['href'])
            if 'ago' in Date:
                newEntry = Cc(handle=handler, date=date.today())
                newEntry.save()
            else:
                newEntry = Cc(handle=handler, date=parse(ccDate(x['href'])).date())
                newEntry.save()
            
    handler.last_sync = date.today().strftime('%Y-%m-%d')
    handler.totalCC = Cc.objects.filter(handle_id=handler.pk).count()
    handler.totalSJ = Sj.objects.filter(handle_id=handler.pk).count()
    handler.totalCF = Cf.objects.filter(handle_id=handler.pk).count()
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
            newEntry = Cf(handle=handler, date=parse(info[0].text.strip()).date())
            newEntry.save()
    handler.last_sync = date.today().strftime('%Y-%m-%d')
    handler.totalCC = Cc.objects.filter(handle_id=handler.pk).count()
    handler.totalSJ = Sj.objects.filter(handle_id=handler.pk).count()
    handler.totalCF = Cf.objects.filter(handle_id=handler.pk).count()
    handler.save()
    print('success cf', entry)

@shared_task
def codeforceCrawler(username):
    url = 'https://codeforces.com/submissions/' + username
    uClient = uReq(url)
    html = uClient.read()
    uClient.close()
    page = soup(html, 'lxml')
    # maxIndex = page.find(lambda tag: tag.name == 'div' and tag.get('class') == ['pagination']).ul
    maxIndex = [int(x.text) for x in page.findAll('span', class_='page-index')]
    maxId = 1
    if maxIndex:
        maxId = max(maxIndex)
    if maxId < 129:
        data(url, maxId, username)

@shared_task
def updater(handle):
	handler = User.objects.get(name_exact=handle)
	handler.totalCC = Cc.objects.filter(handle_id=handler.pk).count()
	handler.totalSJ = Sj.objects.filter(handle_id=handler.pk).count()
	handler.totalCF = Cf.objects.filter(handle_id=handler.pk).count()
	handler.save()