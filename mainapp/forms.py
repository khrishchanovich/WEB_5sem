from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *
import re


class InsuranceTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = InsuranceType
        fields = '__all__'


class ContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Вид страхования не выбран'
        self.fields['ins_object'].empty_label = 'Объект страхования не выбран'
        self.fields['address'].empty_label = 'Филиал не выбран'

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        pattern = r'^\+375\d{9}$'
        if not re.match(pattern, phone_number):
            raise ValidationError('Номер телефона должен быть представлен в формате: +375*********')

        return phone_number

    def clean_initial_payment(self):
        initial_payment = self.cleaned_data['initial_payment']

        if initial_payment < 10:
            raise ValidationError('Первоначальный взнос должен быть больше 10 рублей')

        return initial_payment

    class Meta:
        model = Contract
        fields = ['last_name',
                  'name',
                  'middle_name',
                  'email',
                  'phone_number',
                  'cat',
                  'ins_object',
                  'address',
                  'accept_terms',
                  'initial_payment']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'forms-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'forms-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'forms-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'forms-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'forms-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'forms-input'}))


class FAQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].empty_label = 'Вопрос не введен'
        self.fields['answer'].empty_label = 'Ответ не введен'

    class Meta:
        model = FAQ
        fields = ['question',
                  'answer']


class FeedBackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].empty_label = 'Имя не введено'
        self.fields['last_name'].empty_label = 'Фамилия не введена'
        self.fields['rating'].empty_label = 'Вы не поставили оценку'
        self.fields['feedback'].empty_label = 'Вы не оставили отзыв'

    def clean_feedback(self):
        feedback = self.cleaned_data['feedback']

        if len(feedback) <= 0:
            raise ValidationError('Отзыв не был введен')

        return feedback

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) <= 0:
            raise ValidationError('Имя не введено')

        return name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if len(last_name) <= 0:
            raise ValidationError('Фамилия не введена')

        return last_name

    class Meta:
        model = FeedBack
        fields = ['name',
                  'last_name',
                  'rating',
                  'feedback']

