from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from collections import OrderedDict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from accounts.models import User
from .forms import (
    UserProfileForm,
    TargetForm,
    AchievementLevelForm,
    LifeStyleForm,
)
from .models import Target, LifeStyle, Category
from .services.category import get_parent_categories, get_child_categories
from .services.target import create_target, update_achievement_level
from .services.lifestyle import create_lifestyle, list_lifestyles, update_lifestyle
from .services.radarchart import generate_band_chart_data, generate_band_chart_data_for_date


def top(request):
    return render(request, "healthapp/index.html")

def home(request):
    chart_data = {"groups": [], "legend": []}
    if request.user.is_authenticated:
        chart_data = generate_band_chart_data(request.user)
    return render(request, 'healthapp/home.html', {"chart_data": chart_data})


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


@login_required
def lifestyle(request):
    notice = ""
    parents = list(get_parent_categories())
    category_groups = [(parent, list(get_child_categories(parent))) for parent in parents]
    allowed_category_ids = {
        child.id for _, children in category_groups for child in children
    }

    rows = [{"category_id": "", "time": "", "content": ""}]
    date_value = date.today()

    if request.method == "POST":
        date_str = request.POST.get("date", "").strip()
        date_value = parse_date(date_str) if date_str else None

        category_ids = request.POST.getlist("category")
        times = request.POST.getlist("time")
        contents = request.POST.getlist("content")

        max_len = max(len(category_ids), len(times), len(contents), 1)
        rows = []
        valid_rows = []

        for i in range(max_len):
            category_id = category_ids[i] if i < len(category_ids) else ""
            time_value = times[i] if i < len(times) else ""
            content_value = contents[i] if i < len(contents) else ""
            rows.append(
                {
                    "category_id": category_id,
                    "time": time_value,
                    "content": content_value,
                }
            )

            if not category_id and not time_value and not content_value:
                continue

            if not category_id or not time_value:
                notice = "カテゴリと時間は必須です。"
                continue

            if not category_id.isdigit() or int(category_id) not in allowed_category_ids:
                notice = "カテゴリを正しく選択してください。"
                continue

            try:
                time_decimal = Decimal(time_value)
                if time_decimal < 0:
                    raise ValueError
                if time_decimal.as_tuple().exponent < -1:
                    raise ValueError
                time_decimal = time_decimal.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            except (InvalidOperation, ValueError):
                notice = "時間は0以上で小数第1位まで入力してください。"
                continue

            valid_rows.append(
                {
                    "category_id": int(category_id),
                    "time": time_decimal,
                    "content": content_value,
                }
            )

        if not date_value:
            notice = "日付を入力してください。"
        elif not valid_rows:
            if not notice:
                notice = "少なくとも1件の行動を入力してください。"
        else:
            total_time = sum((row["time"] for row in valid_rows), Decimal("0.0"))
            if total_time != Decimal("24.0"):
                notice = "1日の合計時間は24.0時間にしてください。"
            else:
                categories = Category.objects.in_bulk(
                    [row["category_id"] for row in valid_rows]
                )
                for row in valid_rows:
                    create_lifestyle(
                        user=request.user,
                        date=date_value,
                        category=categories[row["category_id"]],
                        time=row["time"],
                        content=row["content"],
                    )
                return redirect("healthapp:lifestyle")

    items = list_lifestyles(request.user)
    grouped_items = OrderedDict()
    for item in items:
        grouped_items.setdefault(item.date, []).append(item)
    return render(
        request,
        "healthapp/lifestyle.html",
        {
            "items": items,
            "grouped_items": grouped_items.items(),
            "notice": notice,
            "category_groups": category_groups,
            "rows": rows,
            "date_value": date_value,
        },
    )


@login_required
def lifestyle_detail(request, date):
    date_value = parse_date(date)
    if not date_value:
        return redirect("healthapp:lifestyle")

    parents = list(get_parent_categories())
    category_groups = [(parent, list(get_child_categories(parent))) for parent in parents]
    allowed_category_ids = {
        child.id for _, children in category_groups for child in children
    }

    items = list_lifestyles(request.user).filter(date=date_value)
    rows = [
        {
            "category_id": item.category_id,
            "time": item.time,
            "content": item.content,
        }
        for item in items
    ] or [{"category_id": "", "time": "", "content": ""}]

    notice = ""
    if request.method == "POST":
        category_ids = request.POST.getlist("category")
        times = request.POST.getlist("time")
        contents = request.POST.getlist("content")

        max_len = max(len(category_ids), len(times), len(contents), 1)
        rows = []
        valid_rows = []

        for i in range(max_len):
            category_id = category_ids[i] if i < len(category_ids) else ""
            time_value = times[i] if i < len(times) else ""
            content_value = contents[i] if i < len(contents) else ""
            rows.append(
                {
                    "category_id": category_id,
                    "time": time_value,
                    "content": content_value,
                }
            )

            if not category_id and not time_value and not content_value:
                continue

            if not category_id or not time_value:
                notice = "カテゴリと時間は必須です。"
                continue

            if not category_id.isdigit() or int(category_id) not in allowed_category_ids:
                notice = "カテゴリを正しく選択してください。"
                continue

            try:
                time_decimal = Decimal(time_value)
                if time_decimal < 0:
                    raise ValueError
                if time_decimal.as_tuple().exponent < -1:
                    raise ValueError
                time_decimal = time_decimal.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            except (InvalidOperation, ValueError):
                notice = "時間は0以上で小数第1位まで入力してください。"
                continue

            valid_rows.append(
                {
                    "category_id": int(category_id),
                    "time": time_decimal,
                    "content": content_value,
                }
            )

        if not valid_rows:
            if not notice:
                notice = "少なくとも1件の行動を入力してください。"
        else:
            total_time = sum((row["time"] for row in valid_rows), Decimal("0.0"))
            if total_time != Decimal("24.0"):
                notice = "1日の合計時間は24.0時間にしてください。"
            else:
                categories = Category.objects.in_bulk(
                    [row["category_id"] for row in valid_rows]
                )
                LifeStyle.objects.filter(user=request.user, date=date_value).delete()
                for row in valid_rows:
                    create_lifestyle(
                        user=request.user,
                        date=date_value,
                        category=categories[row["category_id"]],
                        time=row["time"],
                        content=row["content"],
                    )
                return redirect("healthapp:lifestyle_detail", date=date)

    chart_data = generate_band_chart_data_for_date(request.user, date_value)
    return render(
        request,
        "healthapp/lifestyle_detail.html",
        {
            "rows": rows,
            "notice": notice,
            "category_groups": category_groups,
            "date_value": date_value,
            "chart_data": chart_data,
        },
    )

def analysis(request):
    return render(request, "healthapp/analysis.html")
