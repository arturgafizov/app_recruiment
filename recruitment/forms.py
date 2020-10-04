from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from recruitment.models import Vacancy
from recruitment.models import Application
from recruitment.models import Company
from recruitment.models import Resume


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter',)


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count', 'logo',)
#        CompanyFormSet = inlineformset_factory(Company, fields='__all__')

class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max',)


class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ('name', 'surname', 'status', 'salary', 'grade', 'edication', 'experience', 'portfolio', )


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
    help_text = {
        'username': 'Требование к логину. Не более 150 символов. И только буквы, цифры и символы @/./+/-/_.'
    }


class UserProfileForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = None
    class Meta:
        model = User
        fields = ['first_name', 'last_name', "email"]
    help_text = {
        'username': 'Требование к логину. Не более 150 символов. И только буквы, цифры и символы @/./+/-/_.'
    }
