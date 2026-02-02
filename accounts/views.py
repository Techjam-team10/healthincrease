from django.http import HttpResponse


def signin(request):
    return HttpResponse("signin")


def signup(request):
    return HttpResponse("signup")


def signout(request):
    return HttpResponse("signout")
