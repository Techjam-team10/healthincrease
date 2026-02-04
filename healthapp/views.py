from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .forms import UserProfileForm, TargetForm, AchievementLevelForm
from .models import Target
from .services.target import create_target, update_achievement_level


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
    from django.shortcuts import redirect
    from accounts.models import User
    from healthapp.models import Post
    from healthapp.services.timeline import create_post, get_timeline_posts, increment_favorite

    notice = ""
    user = User.objects.first()
    liked_post_ids = set(request.session.get("liked_post_ids", []))

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            content = request.POST.get("content", "").strip()
            if not user:
                notice = "投稿にはユーザーが必要です。"
            elif content:
                create_post(user=user, content=content)
                return redirect("healthapp:timeline")
            else:
                notice = "投稿内容を入力してください。"
        elif action == "favorite":
            post_id = request.POST.get("post_id")
            if post_id:
                post_id_int = int(post_id)
                if post_id_int in liked_post_ids:
                    notice = "いいねは一人1回までです。"
                else:
                    post = Post.objects.filter(pk=post_id_int).first()
                    if post:
                        increment_favorite(post)
                        liked_post_ids.add(post_id_int)
                        request.session["liked_post_ids"] = list(liked_post_ids)
                        return redirect("healthapp:timeline")

    posts = get_timeline_posts(limit=None)
    return render(
        request,
        "healthapp/timeline.html",
        {
            "posts": posts,
            "notice": notice,
            "has_user": bool(user),
            "liked_post_ids": list(liked_post_ids),
        },
    )


def timeline_detail(request, post_id):
    from django.shortcuts import redirect
    from accounts.models import User
    from healthapp.models import Comment, Post
    from healthapp.services.timeline import increment_favorite

    notice = ""
    user = User.objects.first()
    post = Post.objects.select_related("user").filter(pk=post_id).first()
    liked_post_ids = set(request.session.get("liked_post_ids", []))

    if request.method == "POST" and post:
        action = request.POST.get("action")
        if action == "favorite":
            if post.id in liked_post_ids:
                notice = "いいねは一人1回までです。"
            else:
                increment_favorite(post)
                liked_post_ids.add(post.id)
                request.session["liked_post_ids"] = list(liked_post_ids)
                return redirect("healthapp:timeline_detail", post_id=post_id)
        if action == "comment":
            content = request.POST.get("content", "").strip()
            if not user:
                notice = "コメントにはユーザーが必要です。"
            elif content:
                Comment.objects.create(post=post, user=user, content=content)
                return redirect("healthapp:timeline_detail", post_id=post_id)
            else:
                notice = "コメント内容を入力してください。"

    comments = (
        Comment.objects.select_related("user").filter(post=post).order_by("created_at")
        if post
        else []
    )
    return render(
        request,
        "healthapp/timeline_detail.html",
        {
            "post": post,
            "comments": comments,
            "notice": notice,
            "has_user": bool(user),
            "liked_post_ids": list(liked_post_ids),
        },
    )


@login_required
def target(request):
    targets = Target.objects.filter(user=request.user).order_by("term", "id")
    return render(request, "healthapp/target.html", {"targets": targets})


@login_required
def target_detail(request, target_id):
    target = get_object_or_404(Target, pk=target_id, user=request.user)
    achievement_form = AchievementLevelForm(instance=target)
    return render(
        request,
        "healthapp/target_detail.html",
        {"target": target, "achievement_form": achievement_form},
    )


@login_required
def target_create(request):
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data["term"]
            content = form.cleaned_data["content"]
            target = create_target(user=request.user, term=term, content=content)
            return redirect("healthapp:target_detail", target_id=target.id)
    else:
        form = TargetForm()
    return render(request, "healthapp/target_create.html", {"form": form})


@login_required
def target_edit(request, target_id):
    target = get_object_or_404(Target, pk=target_id, user=request.user)
    if request.method == "POST":
        form = TargetForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            return redirect("healthapp:target_detail", target_id=target.id)
    else:
        form = TargetForm(instance=target)
    return render(
        request,
        "healthapp/target_edit.html",
        {"form": form, "target": target},
    )


@login_required
def update_achievement(request, target_id):
    target = get_object_or_404(Target, pk=target_id, user=request.user)
    if request.method != "POST":
        return redirect("healthapp:target_detail", target_id=target.id)

    form = AchievementLevelForm(request.POST, instance=target)
    if form.is_valid():
        update_achievement_level(target, form.cleaned_data["achievement_level"])
        return redirect("healthapp:target_detail", target_id=target.id)

    return render(
        request,
        "healthapp/target_detail.html",
        {"target": target, "achievement_form": form},
    )


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
