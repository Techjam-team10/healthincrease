from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .forms import UserProfileForm


def top(request):
    return render(request, "healthapp/index.html")

def home(request):
    return render(request, 'healthapp/home.html')


@login_required
def profile(request):
    user = request.user
    context = {
        'profile_user': user
    }
    return render(request, "healthapp/profile.html", context)


@login_required
def profile_setting(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # ログインユーザーが自分のプロフィール以外は編集不可
    if request.user.id != user.id:
        return redirect('healthapp:profile_detail', user_id=user_id)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('healthapp:profile')
    else:
        form = UserProfileForm(instance=user)
    
    context = {
        'form': form,
        'profile_user': user
    }
    return render(request, "healthapp/profile_setting.html", context)


def profile_detail(request, user_id):
    return render(request, "healthapp/profile_detail.html", {"user_id": user_id})


def timeline(request):
    return render(request, "healthapp/timeline.html")


def timeline_detail(request, post_id):
    return render(request, "healthapp/timeline_detail.html", {"post_id": post_id})


def target(request):
    return render(request, "healthapp/target.html")


def target_detail(request, term_id):
    return render(request, "healthapp/target_detail.html", {"term_id": term_id})


def lifestyle(request):
    return render(request, "healthapp/lifestyle.html")


def lifestyle_date(request, date):
    return render(request, "healthapp/lifestyle_date.html", {"date": date})


def lifestyle_detail(request, date):
    return render(request, "healthapp/lifestyle_detail.html", {"date": date})


def lifestyle_setdata(request, date):
    return render(request, "healthapp/lifestyle_setdata.html", {"date": date})

def analysis(request):
    return render(request, "healthapp/analysis.html")
