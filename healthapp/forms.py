from django import forms
from accounts.models import User
from .models import Target


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


class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['term', 'content']
        widgets = {
            'term': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'term': '期限',
            'content': '目標内容',
        }


class AchievementLevelForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['achievement_level']
        widgets = {
            'achievement_level': forms.NumberInput(
                attrs={'min': 0, 'max': 100, 'class': 'form-control'}
            ),
        }
        labels = {
            'achievement_level': '達成度 (0-100)',
        }
