from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from hypernews.settings import NEWS_JSON_PATH
import json

class HomeView(View):
    def get(self, request, *args, **kwargs):
        link = kwargs.get('link', None)
        print("Link", link)
        if link:
            news_pages = json.load(open(NEWS_JSON_PATH))
            for page in news_pages:
                if page['link'] == link:
                    return render(request, r"news\news.html", context={'news': page})
            return render(request, r"news\not_found.html", context={'link': link})
        else:
            return render(request, r"news\index.html")
