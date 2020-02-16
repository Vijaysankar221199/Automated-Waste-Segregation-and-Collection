from django import forms
from django.core import validators
from myapp.models import User
from .models import *

class Authentic(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields =("username","password","first_name","last_name")





class friendvis(forms.ModelForm):

    class Meta:
        model = friendvisitor
        fields = ['Type','unit', 'Location']

class urgentvis(forms.ModelForm):

    class Meta:
        model = urgentvisitor
        fields = ['Type','unit', 'Location']
