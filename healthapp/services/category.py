from typing import Optional, Tuple, List, Dict

from django.db.models import QuerySet
from healthapp.models import Category  # 参照先を healthapp に変更

# --- A. カテゴリ関連関数 ---
def get_parent_categories() -> QuerySet[Category]:
    return Category.objects.filter(parent__isnull=True)

def get_child_categories(parent: Category) -> QuerySet[Category]:
    return Category.objects.filter(parent=parent)

def get_category_tree() -> dict:
    tree = {}
    parents = get_parent_categories()
    for p in parents:
        tree[p] = list(get_child_categories(p))
    return tree


CATEGORY ={"運動": ["スポーツ", "力仕事", "歩く"], "休息": ["睡眠", "動画視聴", "ゲーム"],  "思考": ["勉強", "デスクワーク", "読書"], "食事": ["朝食", "昼食", "間食", "夕食"]}


def get_category_groups() -> List[Dict[str, List[Dict[str, str]]]]:
    return [
        {
            "parent": parent,
            "children": [
                {"title": child, "value": build_category_value(parent, child)}
                for child in children
            ],
        }
        for parent, children in CATEGORY.items()
    ]


def build_category_value(parent_title: str, child_title: str) -> str:
    return f"{parent_title}::{child_title}"


def parse_category_value(value: str) -> Optional[Tuple[str, str]]:
    if not value or "::" not in value:
        return None
    parent_title, child_title = value.split("::", 1)
    if parent_title not in CATEGORY:
        return None
    if child_title not in CATEGORY[parent_title]:
        return None
    return parent_title, child_title


def get_allowed_category_values() -> set:
    return {
        build_category_value(parent, child)
        for parent, children in CATEGORY.items()
        for child in children
    }


def find_parent_by_child(child_title: str) -> Optional[str]:
    for parent, children in CATEGORY.items():
        if child_title in children:
            return parent
    return None


def category_to_value(category: Category) -> Optional[str]:
    if category.parent:
        parent_title = category.parent.title
        child_title = category.title
    else:
        parent_title = find_parent_by_child(category.title)
        child_title = category.title
    if not parent_title:
        return None
    if child_title not in CATEGORY.get(parent_title, []):
        return None
    return build_category_value(parent_title, child_title)