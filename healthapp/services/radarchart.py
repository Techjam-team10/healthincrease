from decimal import Decimal
from typing import List, Dict

from healthapp.models import LifeStyle
from .category import CATEGORY, find_parent_by_child


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
    """
    帯グラフ表示用データを生成する
    返り値: {
      "groups": [
        {"date": date, "segments": [{"label": str, "hours": Decimal, "percent": float, "color": str}, ...]},
      ],
      "legend": [{"label": str, "color": str}, ...]
    }
    """
    parent_titles = list(CATEGORY.keys())
    color_map = {
        parent: COLOR_PALETTE[i % len(COLOR_PALETTE)]
        for i, parent in enumerate(parent_titles)
    }

    date_list = list(
        LifeStyle.objects.filter(user=user)
        .values_list("date", flat=True)
        .distinct()
        .order_by("-date")[:limit_days]
    )
    date_list = list(reversed(date_list))

    groups: List[Dict] = []

    for day in date_list:
        items = (
            LifeStyle.objects.filter(user=user, date=day)
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

        groups.append({"date": day, "segments": segments})

    legend = [{"label": parent, "color": color_map[parent]} for parent in parent_titles]
    return {"groups": groups, "legend": legend}


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