# coding:utf-8
from django import forms
from .models import MyUser

class RegistForm(forms.ModelForm):
    """用户注册"""

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



