import datetime
import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
import books.models


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='User name',
        max_length=30
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Password again',
        widget=forms.PasswordInput()
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords mismatch.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain letters, numbers, and underscores.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username already in use.')


class BookSaveForm(forms.Form):
    title = forms.CharField(label='Title', max_length=books.models.MAX_BOOK_TITLE_LEN, required=False)
    isbn = forms.CharField(label='ISBN', max_length=books.models.ISBN_DIGITS)
    author = forms.CharField(label='Author', max_length=books.models.MAX_AUTHOR_LEN, required=False)
    publisher = forms.CharField(label='Publisher', max_length=books.models.MAX_PUBLISHER_LEN, required=False)
    memo = forms.CharField(label='memo', widget=forms.Textarea(), required=False)
    star1 = forms.ChoiceField(choices=[(0, 'Cancel'), (2, '1 star'), (4, '2 stars'), (6, '3 stars'), (8, '4 stars'), (10, '5 stars')], required=False)
    check1 = forms.BooleanField(label='check1', required=False)
    check2 = forms.BooleanField(label='check2', required=False)
    check3 = forms.BooleanField(label='check3', required=False)
    dateStart = forms.DateField(label='DateStart', required=False)
    dateEnd = forms.DateField(label='DateEnd', initial=datetime.date.today, required=False)
    tags = forms.CharField(label='Tags', required=False)
    link = forms.CharField(label='link', required=False)
    imageLink = forms.CharField(label='imageLink', required=False)
