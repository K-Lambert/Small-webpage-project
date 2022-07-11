from django import forms
from django.contrib.auth.models import User
from AppOne.models import *

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('username', 'password')


class RegistrationForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email', 'groups')


class RegistrationExtensionForm(forms.ModelForm):
    class Meta():
        model = UserClassExtension
        fields = ('User','class_id')


class TaskForm(forms.ModelForm):
    class Meta():
        model = TaskModel
        fields = ('task_name', 'task_description', 'task_add_date')
