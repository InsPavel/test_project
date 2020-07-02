from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm


class UserCreationForm(BSModalModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтверждение пароля", strip=False, widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            print(error)
            self.add_error('password', error)
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        return super().save()

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']
