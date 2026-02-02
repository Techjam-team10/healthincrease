from django.http import HttpResponse


def top(request):
    return HttpResponse("top")


def profile(request):
    return HttpResponse("profile")


def profile_setting(request, user_id):
    return HttpResponse(f"profile_setting user_id={user_id}")


def profile_detail(request, user_id):
    return HttpResponse(f"profile_detail user_id={user_id}")


def timeline(request):
    return HttpResponse("timeline")


def timeline_detail(request, post_id):
    return HttpResponse(f"timeline_detail post_id={post_id}")


def target(request):
    return HttpResponse("target")


def target_detail(request, term_id):
    return HttpResponse(f"target_detail term_id={term_id}")


def lifestyle(request):
    return HttpResponse("lifestyle")


def lifestyle_date(request, date):
    return HttpResponse(f"lifestyle_date date={date}")


def lifestyle_detail(request, date):
    return HttpResponse(f"lifestyle_detail date={date}")


def lifestyle_setdata(request, date):
    return HttpResponse(f"lifestyle_setdata date={date}")
