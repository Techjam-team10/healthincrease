
from django.contrib import admin
from .models import Category, LifeStyle

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # リーダーの設計名(title, parent)に合わせて表示
    list_display = ('id', 'title', 'parent')

@admin.register(LifeStyle)
class LifeStyleAdmin(admin.ModelAdmin):
    # リーダーの設計名(date, user, category, time)に合わせて表示
    list_display = ('date', 'user', 'category', 'time')
