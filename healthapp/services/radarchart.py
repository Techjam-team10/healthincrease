# --- D. レーダーチャート用 ---
from django.db.models import Sum
from healthapp.models import Category, LifeStyle, RadarChartData
from datetime import date

def generate_radar_chart_data(user, start_date: date, end_date: date) -> list:
    """
    レーダーチャート表示用データを生成する
    返り値: [ { "category": Category, "actual": int, "ideal": int, "diff": int }, ... ]
    """
    logs = (
        LifeStyle.objects.filter(user=user, date__range=[start_date, end_date])
        .values('category')
        .annotate(total_time=Sum('time'))
    )
    
    actual_times = {log['category']: log['total_time'] for log in logs}
    total_minutes = sum(actual_times.values())
    results = []

    for cat in Category.objects.all():
        actual_percent = 0
        if total_minutes > 0:
            actual_time = actual_times.get(cat.id, 0)
            actual_percent = int(round((actual_time / total_minutes) * 100))
        
        # モデルに ideal_percentage を追加していない場合は、一旦 0 や固定値で対応
        ideal_percent = getattr(cat, 'ideal_percentage', 0)
        
        results.append({
            "category": cat,
            "actual": actual_percent,
            "ideal": ideal_percent,
            "diff": actual_percent - ideal_percent
        })
    return results

def save_radar_data(user, category: Category, value: int) -> RadarChart:
    """レーダーチャート値を保存または更新する"""
    radar_data, _ = RadarChartData.objects.update_or_create(
        user=user,
        category=category,
        defaults={"value": value}
    )
    return radar_data