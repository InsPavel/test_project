from django.urls import path
from webapp.views import IndexView, ArticleDetailView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
]
