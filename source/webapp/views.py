from django.views.generic import ListView, DetailView
from webapp.models import Article


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    template_name = 'article/article_view.html'
    model = Article
    context_object_name = 'article'



