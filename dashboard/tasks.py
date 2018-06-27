import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from .models import User, Sj, Cc, Cf
from dateutil.parser import parse
from datetime import date, datetime

def getDate(url):
	uClient = uReq('http://www.spoj.com' + url)
	html = uClient.read()
	uClient.close()
	page = soup(html, 'lxml')
	date = page.find('td', class_='status_sm')
	return date.span.text

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
    handler.totalSJ = entry
    handler.save()
    print('success spoj')
    
def ccDate(url):
	page  = requests.get('https://www.codechef.com'+url)
	souper=soup(page.content, 'lxml')
	table = souper.find('table', class_='dataTable').tbody.tr
	table = table.findAll('td')
	return table[1].text

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
            newEntry = Cc(handle=handler, date=parse(ccDate(x['href'])).date())
            newEntry.save()
    handler.totalCC = entry
    handler.save()
    print('success cc')

def data(url, index, username):
    handler = User.objects.get(codeforce__exact=username)
    for x in range(1,index+1):
        uClient = uReq(url+'/page/'+str(x))
        html = uClient.read()
        uClient.close()
        page = soup(html, 'lxml')
        content = page.find('table', class_='status-frame-datatable')
        content = content.findAll('tr')
        entry = 0
        content.pop(0)
        for x in content:
            info = x.findAll('td', class_='status-small')
            entry = entry +1
            newEntry = Cf(handle=handler, date=parse(info[0].text.strip()).date())
            newEntry.save()
        handler.totalCF = entry
        handler.last_sync = date.today().strftime('%Y-%m-%d')
        handler.save()
        print('success cf')


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

