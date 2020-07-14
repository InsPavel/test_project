from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ArticleCreateForm, CategoryForm
from webapp.models import Article, Category
from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalCreateView, BSModalUpdateView


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


class ArticleDeleteView(BSModalDeleteView):
    model = Article
    template_name = 'article/article_delete.html'
    success_message = 'Вы успешно удалили статью'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'article'


class CategoriesListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(BSModalCreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_create.html'
    success_url = reverse_lazy('webapp:categories')
    success_message = 'Категория успешно добавлена'


class CategoryUpdateView(BSModalUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_update.html'
    success_url = reverse_lazy('webapp:categories')
    success_message = 'Категория успешно обновлена'
    context_object_name = 'category'


class CategoryDeleteView(BSModalDeleteView):
    model = Category
    template_name = 'category/category_delete.html'
    success_message = 'Вы успешно удалили категорию'
    success_url = reverse_lazy('webapp:categories')
    context_object_name = 'category'






