from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm


def signin(request):
    if request.user.is_authenticated:
        return redirect('healthapp:home')
    
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'ログインしました。')
            return redirect('healthapp:home')
        else:
            messages.error(request, 'ユーザー名またはパスワードが正しくありません。')
    else:
        form = SignInForm()
    
    return render(request, "accounts/signin.html", {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ユーザーをログイン
            login(request, user)
            messages.success(request, '会員登録が完了しました。')
            return redirect('healthapp:home')
        else:
            # フォームエラーをメッセージに追加
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    
    return render(request, "accounts/signup.html", {'form': form})


def signout(request):
    return render(request,"accounts/signout.html")
