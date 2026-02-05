from decimal import Decimal
from typing import List, Dict
from healthapp.models import LifeStyle, Category
from .category import CATEGORY, find_parent_by_child
from healthapp.models import IdealTimeAllocation


COLOR_PALETTE = [
    "#4C9AFF",
    "#36B37E",
    "#FF8B00",
    "#6554C0",
    "#FF5630",
    "#00B8D9",
    "#0052CC",
    "#00875A",
]



def generate_band_chart_data(user, limit_days: int = 7) -> Dict:
    # 親カテゴリをDBから取得（ここが基準）
    parents = Category.objects.filter(parent__isnull=True).order_by("id")

    # 色割り当て（表示順は CATEGORY.keys() を基準にする）
    parent_titles = list(CATEGORY.keys())
    color_map = {
        title: COLOR_PALETTE[i % len(COLOR_PALETTE)]
        for i, title in enumerate(parent_titles)
    }

    # 表示対象日（直近 limit_days 日）
    date_list = list(
        LifeStyle.objects.filter(user=user)
        .values_list("date", flat=True)
        .distinct()
        .order_by("-date")[:limit_days]
    )
    date_list = list(reversed(date_list))

    groups: List[Dict] = []

    # =========================
    # 実績（通常の帯グラフ）
    # =========================
    for day in date_list:
        items = (
            LifeStyle.objects.filter(user=user, date=day)
            .select_related("category", "category__parent")
        )

        totals = {parent.title: Decimal("0.0") for parent in parents}

        for item in items:
            if item.category.parent:
                parent_title = item.category.parent.title
            else:
                parent_title = item.category.title

            if parent_title in totals:
                totals[parent_title] += item.time

        segments = []
        for parent in parents:
            hours = totals[parent.title]
            percent = float((hours / Decimal("24.0")) * 100) if hours else 0.0

            segments.append({
                "label": parent.title,
                "hours": hours,
                "percent": percent,
                "color": color_map.get(parent.title),
            })

        groups.append({
            "date": day,
            "segments": segments,
        })

    # =========================
    # 理想時間（帯グラフ・1行目）
    # =========================
    ideal_map = {
        i.category_id: i.ideal_hours
        for i in IdealTimeAllocation.objects.filter(user=user)
    }

    ideal_segments = []
    for parent in parents:
        hours = ideal_map.get(parent.id, Decimal("0"))
        percent = float((hours / Decimal("24.0")) * 100) if hours else 0.0

        ideal_segments.append({
            "label": parent.title,
            "hours": hours,
            "percent": percent,
            "color": color_map.get(parent.title),
            "is_ideal": True,
        })

    groups.insert(0, {
        "date": "理想",
        "segments": ideal_segments,
        "is_ideal": True,
    })

    # =========================
    # legend（親カテゴリのみ）
    # =========================
    legend = [
        {
            "label": parent.title,
            "color": color_map.get(parent.title),
            "category_id": parent.id,
        }
        for parent in parents
    ]

    return {
        "groups": groups,
        "legend": legend,
    }

def generate_band_chart_data_for_date(user, target_date) -> Dict:
    """
    特定日の帯グラフ表示用データを生成する
    """
    parent_titles = list(CATEGORY.keys())
    color_map = {
        parent: COLOR_PALETTE[i % len(COLOR_PALETTE)]
        for i, parent in enumerate(parent_titles)
    }

    items = (
        LifeStyle.objects.filter(user=user, date=target_date)
        .select_related("category", "category__parent")
        .order_by("id")
    )

    totals = {parent: Decimal("0.0") for parent in parent_titles}
    for item in items:
        if item.category.parent:
            parent_title = item.category.parent.title
        else:
            parent_title = find_parent_by_child(item.category.title) or item.category.title
        if parent_title not in totals:
            continue
        totals[parent_title] += item.time

    segments = []
    for parent in parent_titles:
        hours = totals.get(parent, Decimal("0.0"))
        percent = float((hours / Decimal("24.0")) * 100) if hours else 0.0
        segments.append(
            {
                "label": parent,
                "hours": hours,
                "percent": percent,
                "color": color_map[parent],
            }
        )

    legend = [{"label": parent, "color": color_map[parent]} for parent in parent_titles]
    return {"group": {"date": target_date, "segments": segments}, "legend": legend}