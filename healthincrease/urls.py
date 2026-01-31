from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def simple_view(name):
    def view(request, **kwargs):
        parts = [name]
        if kwargs:
            parts.append(" ".join(f"{key}={value}" for key, value in kwargs.items()))
        return HttpResponse(" | ".join(parts))

    return view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', simple_view('top'), name='top'),
    path('top/', simple_view('top'), name='top_redirect'),
    path('signin/', simple_view('signin'), name='signin'),
    path('signup/', simple_view('signup'), name='signup'),
    path('signout/', simple_view('signout'), name='signout'),
    path('profile/', simple_view('profile'), name='profile'),
    path('profile/<int:user_id>/setting/', simple_view('profile_setting'), name='profile_setting'),
    path('profile/<int:user_id>/', simple_view('profile_detail'), name='profile_detail'),
    path('timeline/', simple_view('timeline'), name='timeline'),
    path('timeline/<int:post_id>/', simple_view('timeline_detail'), name='timeline_detail'),
    path('target/', simple_view('target'), name='target'),
    path('target/<int:term_id>/', simple_view('target_detail'), name='target_detail'),
    path('lifestyle/', simple_view('lifestyle'), name='lifestyle'),
    path('lifestyle/<str:date>/', simple_view('lifestyle_date'), name='lifestyle_date'),
    path('lifestyle/<str:date>/detail/', simple_view('lifestyle_detail'), name='lifestyle_detail'),
    path('lifestyle/<str:date>/setdata/', simple_view('lifestyle_setdata'), name='lifestyle_setdata'),
]
