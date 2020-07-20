from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView
from .forms import UserCreationForm, PasswordChangeForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView


class RegisterView(BSModalCreateView):
    template_name = 'partial/user_create.html'
    form_class = UserCreationForm
    success_message = 'Вы успешно зарегистрировались. Теперь вы можете авторизоваться.'
    success_url = reverse_lazy('accounts:login')


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


class UserPasswordChangeView(BSModalUpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    success_message = 'Вы успешно сменили пароль. Теперь вы можете авторизоваться.'
    success_url = reverse_lazy('accounts:login')
    context_object_name = 'user_obj'
