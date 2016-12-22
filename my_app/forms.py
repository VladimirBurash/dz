from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Show
from django.contrib.admin.widgets import AdminDateWidget


class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SignupForm(forms.Form):
    login = forms.CharField(label='Login', min_length=5)
    email = forms.CharField(label='Email')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    password = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login):
            raise ValidationError('Этот login уже занят')
        return login

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email( self.cleaned_data['email'])
        if User.objects.filter(email=email):
            raise ValidationError('Этот email уже зарегистрирован')
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        if self.cleaned_data.get('password') and self.cleaned_data.get('repeat_password'):
            if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
                raise ValidationError('Пароли не совпадают')
        return cleaned_data

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['login'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'],
                                        )
        return user


class AddShow(forms.Form):
    groups = forms.CharField(label='Groups',max_length=45,widget=forms.widgets.TextInput, min_length=5)
    place = forms.CharField(label='Place',max_length=45,widget=forms.widgets.TextInput)
    datetime = forms.DateTimeField(label='Datetime',widget=AdminDateWidget)
    image = forms.FileField(required=False,widget=forms.widgets.ClearableFileInput(attrs={
                'accept': 'image/jpeg, image/png, image/gif, image/jpg'
            }))

    def clean_groups(self):
        g = ['Каста','Чаян Фамали','ГРОТ','Макс Корж']
        groups = self.cleaned_data['groups']
        if groups not in g:
            raise ValidationError('Этот login уже занят')
        return groups

    def fill_object(self):
        return Show.objects.create(groups=self.cleaned_data['groups'],
                                   place=self.cleaned_data['place'],
                                   datetime=self.cleaned_data['datetime'])
