from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('healthapp.urls')),
    path('', include('accounts.urls')),
]
