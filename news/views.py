from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from hypernews.settings import NEWS_JSON_PATH
from django import forms
import json


class News(forms.Form):
    title = forms.CharField()
    text = forms.CharField(max_length=2**20)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        news_pages = json.load(open(NEWS_JSON_PATH))
        query = request.GET.get('q', '')
        link = kwargs.get('link', None)
        if link:
            for page in news_pages:
                if page['link'] == link:
                    return render(request, r"news\news.html", context={'news': page})
            return render(request, r"news\not_found.html", context={'link': link})
        else:
            news_by_dates: dict = dict()
            all_news: list = list()
            news_pages = sorted(news_pages, reverse=True, key=lambda x: x['created'])
            for page in news_pages:
                date = page['created']
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                articles = news_by_dates.get(date, [])
                if query in page['title']:
                    articles.append(page)
                news_by_dates[date] = articles
            for date in sorted(news_by_dates.keys(), reverse=True):
                pages = news_by_dates[date]
                if pages:
                    all_news.append({'date': date, 'pages': pages})
            return render(request, r"news\index.html", context={'news_pages': all_news})

class CreateView(View):
    def get(self, request, *args, **kwargs):
        news = News()
        return render(request, r"news\create.html", context={'news': news})
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(NEWS_JSON_PATH) as f:
            news_pages = json.load(f)
        link = int(max(news_pages, key=lambda x: int(x['link']))['link']) + 1
        news = {
            'title': title,
            'text': text,
            'created': date,
            'link': link
        }
        news_pages.append(news)
        with open(NEWS_JSON_PATH, 'w') as f:
            json.dump(news_pages, f, indent=4)
        return redirect('/news/')
