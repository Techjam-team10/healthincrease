from django import forms
from accounts.models import User
from .models import Target, Category, LifeStyle


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


class LifeStyleForm(forms.ModelForm):
    class Meta:
        model = LifeStyle
        fields = ['date', 'category', 'time', 'content']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.NumberInput(
                attrs={'min': 0, 'step': '0.1', 'class': 'form-control'}
            ),
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'date': '日付',
            'category': 'カテゴリ',
            'time': '時間(時間)',
            'content': '内容(任意)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(parent__isnull=False)
