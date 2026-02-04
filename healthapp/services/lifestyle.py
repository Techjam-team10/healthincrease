from django.db.models import QuerySet
from healthapp.models import Category, LifeStyle  # 参照先を healthapp に変更
from accounts.models import User
from datetime import date

# --- B. 行動(LifeStyle)関連関数 ---
def create_lifestyle(user: User, date: date, category: Category, time: int, content: str = "") -> LifeStyle:
    return LifeStyle.objects.create(
        user=user,
        date=date,
        category=category,
        time=time,
        content=content
    )

def get_lifestyle_by_date(user: User, target_date: date) -> QuerySet[LifeStyle]:
    return LifeStyle.objects.filter(user=user, date=target_date)

def aggregate_lifestyle_by_period(user: User, start_date: date, end_date: date) -> dict:
    items = LifeStyle.objects.filter(user=user, date__range=(start_date, end_date))
    summary = {}
    for item in items:
        summary[item.category] = summary.get(item.category, 0) + item.time
    return summary