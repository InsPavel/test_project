from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from webapp.models import Article
from .forms import UserCreationForm, PasswordChangeForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    ordering = ['pk']

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def has_permission(self):
        pk = self.kwargs.get('pk')
        obj = User.objects.get(pk=pk)
        return self.request.user == obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = self.pagination_articles()
        context['page_obj'] = page_obj
        return context

    def pagination_articles(self):
        articles = Article.objects.filter(user_id=self.request.user).order_by('-id')
        paginator = Paginator(articles, 10)
        page = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return page_obj


class RegisterView(BSModalCreateView):
    template_name = 'partial/user_create.html'
    form_class = UserCreationForm
    success_message = 'Вы успешно зарегистрировались. Теперь вы можете авторизоваться.'
    success_url = reverse_lazy('accounts:login')


class UserPasswordChangeView(PermissionRequiredMixin, BSModalUpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    success_message = 'Вы успешно сменили пароль. Теперь вы можете авторизоваться.'
    success_url = reverse_lazy('accounts:login')
    context_object_name = 'user_obj'

    def has_permission(self):
        pk = self.kwargs.get('pk')
        obj = User.objects.get(pk=pk)
        return self.request.user == obj


class UserDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    model = User
    template_name = 'user_delete.html'
    success_message = 'Вы успешно удалили пользователя'
    success_url = reverse_lazy('accounts:user_list')
    context_object_name = 'user'
    permission_required = 'accounts.delete_user'
