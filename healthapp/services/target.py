from datetime import date

from accounts.models import User
from healthapp.models import Target


def create_target(user: User, term: date, content: str) -> Target:
    return Target.objects.create(user=user, term=term, content=content)


def update_achievement_level(target: Target, level: int) -> Target:
    # チーム環境で無効な値が保存されるのを防ぐため、すぐに失敗させます。
    if not 0 <= level <= 100:
        raise ValueError("achievement_level must be between 0 and 100.")
    target.achievement_level = level
    target.save(update_fields=["achievement_level"])
    return target


def is_target_expired(target: Target) -> bool:
    return target.term < date.today()
