from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView
from .forms import UserCreationForm, PasswordChangeForm
from webapp.models import Article
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView


class RegisterView(BSModalCreateView):
    template_name = '../templates/partial/user_create.html'
    form_class = UserCreationForm
    success_message = 'Вы успешно зарегистрировались. Теперь вы можете авторизоваться.'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, request=self.request)
        if form.is_valid():
            return self.form_valid(form)
        return super().post(request, *args, **kwargs)


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


class UserPasswordChangeView(BSModalUpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    success_message = 'Вы успешно сменили пароль. Теперь вы можете авторизоваться.'
    success_url = reverse_lazy('login')
    context_object_name = 'user_obj'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, request=self.request)
        if form.is_valid():
            return self.form_valid(form)
        return super().post(request, *args, **kwargs)


class IndexView(ListView):
    template_name = 'article/index.html'
    model = Article
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    template_name = 'article/article_view.html'
    model = Article
    context_object_name = 'article'



