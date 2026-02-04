from datetime import date
from decimal import Decimal

from django.db.models import QuerySet

from accounts.models import User
from healthapp.models import Category, LifeStyle  # 参照先を healthapp に変更

# --- B. 行動(LifeStyle)関連関数 ---
def create_lifestyle(
    user: User,
    date: date,
    category: Category,
    time: Decimal,
    content: str = "",
    self_evaluation: int = 0,
) -> LifeStyle:
    return LifeStyle.objects.create(
        user=user,
        date=date,
        category=category,
        time=time,
        content=content,
        self_evaluation=self_evaluation,
    )

def get_lifestyle_by_date(user: User, target_date: date) -> QuerySet[LifeStyle]:
    return LifeStyle.objects.filter(user=user, date=target_date)

def aggregate_lifestyle_by_period(user: User, start_date: date, end_date: date) -> dict:
    items = LifeStyle.objects.filter(user=user, date__range=(start_date, end_date))
    summary = {}
    for item in items:
        summary[item.category] = summary.get(item.category, 0) + item.time
    return summary


def list_lifestyles(user: User) -> QuerySet[LifeStyle]:
    return LifeStyle.objects.filter(user=user).order_by("-date", "-id")


def update_lifestyle(
    lifestyle: LifeStyle,
    date_value: date,
    category: Category,
    time: Decimal,
    content: str = "",
    self_evaluation: int = 0,
) -> LifeStyle:
    lifestyle.date = date_value
    lifestyle.category = category
    lifestyle.time = time
    lifestyle.content = content
    lifestyle.self_evaluation = self_evaluation
    lifestyle.save(update_fields=["date", "category", "time", "content", "self_evaluation"])
    return lifestyle