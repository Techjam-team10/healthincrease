from django.db.models import Sum
from ..models import Category, LifeStyle, RadarChart
from datetime import date

# --- C. 分析・可視化 (当初の指定) ---

def calculate_category_ratio(aggregated_data: dict) -> dict:
    """カテゴリ別合計時間から割合（％）を算出する"""
    total_time = sum(aggregated_data.values())
    if total_time == 0:
        return {category: 0 for category in aggregated_data}
    return {
        category: round((time / total_time) * 100)
        for category, time in aggregated_data.items()
    }


def get_ideal_balance() -> dict:
    """
    理想的な行動バランスを取得する
    ※Categoryモデルにideal_percentageを追加している場合はそこから取得
    """
    categories = Category.objects.filter(parent__isnull=True)
    return {
        category: getattr(category, "ideal_percentage", 0)
        for category in categories
    }
    
    # 予備のデフォルト値
    return {"睡眠": 33.3, "仕事": 33.3, "運動": 10.0, "食事": 15.0, "その他": 8.4}

def compare_actual_with_ideal(actual: dict, ideal: dict) -> dict:
    """実績と理想値の差分を計算する"""
    all_categories = set(actual.keys()) | set(ideal.keys())
    return {
        category: actual.get(category, 0) - ideal.get(category, 0)
        for category in all_categories
    }

# --- D. レーダーチャート用 ---

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
