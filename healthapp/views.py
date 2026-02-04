from django.shortcuts import render



def top(request):
    return render(request, "healthapp/index.html")

def home(request):
    return render(request, 'healthapp/home.html')


def profile(request):
    return render(request, "healthapp/profile.html")


def profile_setting(request, user_id):
    return render(request, "healthapp/profile_setting.html", {"user_id": user_id})


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
