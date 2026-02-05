from django.urls import path

from . import views

app_name = 'healthapp'

urlpatterns = [
    path('', views.top, name='top'),
    path('top/', views.top, name='top_redirect'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/setting/', views.profile_setting, name='profile_setting'),
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('timeline/', views.timeline, name='timeline'),
    path('timeline/<int:post_id>/', views.timeline_detail, name='timeline_detail'),
    path('lifestyle/', views.lifestyle, name='lifestyle'),
    path('lifestyle/<str:date>/', views.lifestyle_detail, name='lifestyle_detail'),
    path('analysis/', views.analysis, name='analysis'),
    path("ideal-time/", views.ideal_time_setting, name="ideal_time"),
]
