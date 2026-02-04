from django import forms
from accounts.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'mail']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ユーザー名'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '姓'
            }),
            'mail': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'メールアドレス'
            }),
        }
        labels = {
            'username': 'ユーザー名',
            'first_name': '名',
            'last_name': '姓',
            'mail': 'メールアドレス',
        }
