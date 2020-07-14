from django.urls import path
from webapp.views import IndexView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
]
