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
    path('target/', views.target, name='target'),
    path('target/create/', views.target_create, name='target_create'),
    path('target/<int:target_id>/', views.target_detail, name='target_detail'),
    path('target/<int:target_id>/edit/', views.target_edit, name='target_edit'),
    path('target/<int:target_id>/achievement/', views.update_achievement, name='update_achievement'),
    path('lifestyle/', views.lifestyle, name='lifestyle'),
    path('lifestyle/<str:date>/', views.lifestyle_detail, name='lifestyle_detail'),
    path('analysis/', views.analysis, name='analysis'),
]
