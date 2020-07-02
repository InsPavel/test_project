from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from django.core import validators


class UserCreationForm(BSModalModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields['username'].required = False
        self.fields['username'].validators = [
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                'Введите правильное имя пользователя.'
                ' Это значение может содержать только буквы, цифры и символы @/./+/-/_ .'
            ),
        ]
    password = forms.CharField(label='Пароль', strip=False, required=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подвердите пароль', required=False, strip=False, widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Данное поле обязательное!')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            print(error)
            self.add_error('password', error)
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password_confirm:
            raise forms.ValidationError('Данное поле обязательное!')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Данное поле обязательное!')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError('Пользователь с таким логином уже существует!')
        except User.DoesNotExist:
            return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        return super().save()

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']
