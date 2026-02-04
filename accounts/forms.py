from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    mail = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='パスワード（確認）',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'mail', 'password1', 'password2')

    def clean_mail(self):
        mail = self.cleaned_data.get('mail')
        if User.objects.filter(mail=mail).exists():
            raise forms.ValidationError('このメールアドレスは既に使用されています。')
        return mail

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['mail']
        if commit:
            user.save()
        return user


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('username', 'password')
