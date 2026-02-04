from ..models import Category
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


