import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

requests.packages.urllib3.disable_warnings()

def news_list(request):
    headlines = Headline.objects.all()
    context = {
    	'object_list': headlines,
    }
    return render(request, "news/home.html", context)

def scrape(request):
    session = requests.Session()
    session.verify = False
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://news.abplive.com/news"
    content = session.get(url, verify=True).content
    soup = BSoup(content, "html.parser")
    News = soup.find_all('div', {"class":"other_news"})
    for article in News:
        print(article)
        break
        # check if already exist 
        if not Headline.objects.filter(title__iexact=article.a['title']).exists():
            print("not exist")
            new_headline = Headline()
            new_headline.title = article.a['title']
            new_headline.url = article.a['href']
            new_headline.image = article.img['data-src']
            new_headline.save()
    return redirect("../")

