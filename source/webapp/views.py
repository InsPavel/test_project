from django.shortcuts import render
from django.views.generic import ListView

from webapp.models import Article


class IndexView(ListView):
    template_name = 'article/index.html'
    model = Article
    content_key = 'articles'

