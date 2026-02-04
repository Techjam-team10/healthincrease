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