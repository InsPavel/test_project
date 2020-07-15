from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ArticleCreateForm, CategoryForm
from webapp.models import Article, Category
from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalCreateView, BSModalUpdateView


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = 'articles'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    template_name = 'article/article_view.html'
    model = Article
    context_object_name = 'article'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'article/article_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.pk})


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ['category_id', 'title', 'description', 'image']
    template_name = 'article/article_update.html'
    context_object_name = 'article_obj'

    def has_permission(self):
        pk = self.kwargs.get('pk')
        obj = Article.objects.get(pk=pk)
        if self.request.user.is_staff:
            return True
        return self.request.user == obj.user_id

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    model = Article
    template_name = 'article/article_delete.html'
    success_message = 'Вы успешно удалили статью'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'article'

    def has_permission(self):
        pk = self.kwargs.get('pk')
        obj = Article.objects.get(pk=pk)
        if self.request.user.is_staff:
            return True
        return self.request.user == obj.user_id


class CategoriesListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(PermissionRequiredMixin, BSModalCreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_create.html'
    success_url = reverse_lazy('webapp:categories')
    success_message = 'Категория успешно добавлена'
    permission_required = 'webapp.add_category'


class CategoryUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_update.html'
    success_url = reverse_lazy('webapp:categories')
    success_message = 'Категория успешно обновлена'
    context_object_name = 'category'
    permission_required = 'webapp.change_category'


class CategoryDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    model = Category
    template_name = 'category/category_delete.html'
    success_message = 'Вы успешно удалили категорию'
    success_url = reverse_lazy('webapp:categories')
    context_object_name = 'category'
    permission_required = 'webapp.delete_category'






