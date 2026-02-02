from django.urls import path

from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('top/', views.top, name='top_redirect'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/setting/', views.profile_setting, name='profile_setting'),
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('timeline/', views.timeline, name='timeline'),
    path('timeline/<int:post_id>/', views.timeline_detail, name='timeline_detail'),
    path('target/', views.target, name='target'),
    path('target/<int:term_id>/', views.target_detail, name='target_detail'),
    path('lifestyle/', views.lifestyle, name='lifestyle'),
    path('lifestyle/<str:date>/', views.lifestyle_date, name='lifestyle_date'),
    path('lifestyle/<str:date>/detail/', views.lifestyle_detail, name='lifestyle_detail'),
    path('lifestyle/<str:date>/setdata/', views.lifestyle_setdata, name='lifestyle_setdata'),
]
