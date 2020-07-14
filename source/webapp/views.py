from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ArticleCreateForm
from webapp.models import Article


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    template_name = 'article/article_view.html'
    model = Article
    context_object_name = 'article'


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'article/article_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['category_id', 'title', 'description', 'image']
    template_name = 'article/article_update.html'
    context_object_name = 'article_obj'

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article/article_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'article'







