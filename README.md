# health-increase

行動ログ・目標管理・タイムライン共有を通じて、  
日々の生活習慣を「見える化」し、改善を支援する Web アプリケーションです。

---

## 主な機能

### 行動ログ（LifeStyle）
- 日付ごとの行動記録
- カテゴリ別の時間入力
- 自己評価（0〜100）
- 帯グラフによる可視化

### 目標管理（Target）
- 期限付き目標の作成・編集
- 達成度（％）の更新
- 目標一覧・詳細表示

### 理想の時間配分（設計）
- ユーザー × カテゴリごとの理想時間設定
- 実績との差分算出を想定した設計

### タイムライン
- 投稿の作成・一覧表示
- いいね機能
- コメント機能
- 投稿詳細ページ

### ユーザー管理
- サインアップ / ログイン / ログアウト
- プロフィール表示・編集

---

## 技術スタック

### Backend
- Python
- Django

### Frontend
- Django Templates
- CSS（画面別CSS構成）
- JavaScript（最小限）

### Database
- SQLite（開発環境）
- Django ORM

---

## ディレクトリ構成（抜粋）

```
healthincrease/
├── accounts/
├── healthapp/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── templates/
│ └── static/
│ └── healthapp/
│ ├── css/
│ │ ├── style.css
│ │ ├── home.css
│ │ ├── timeline.css
│ │ └── profile.css
│ └── js/
├── templates/
│ └── base.html
├── db.sqlite3
└── manage.py
```


---

## データモデル概要

### Category
- 親子構造を持つカテゴリ
- 行動ログ・可視化で使用

### LifeStyle
- ユーザーの日次行動ログ
- 実績データ

### Target
- 期限付き目標
- 達成度管理

### Post / Comment
- タイムライン投稿・コメント

### RadarChartData
- ユーザー × カテゴリのスコア（0〜100）
- 可視化用途

---

## セットアップ手順

### 1. リポジトリをクローン

```
git clone https://github.com/Techjam-team10/healthincrease.git
cd healthincrease
```

### 2. 仮想環境作成（任意）

```
python -m venv venv
source venv/bin/activate
```

※ Windows の場合  

```
venv\Scripts\activate
```

### 3. 依存関係のインストール

```
pip install -r requirements.txt
```

### 4. マイグレーション

```
python manage.py migrate
```

### 5. 開発サーバー起動

```
python manage.py runserver
```

---

## 注意事項

- 本リポジトリは開発用途を想定しています
- 本番環境では以下の対応が必要です
  - DEBUG = False
  - 本番用データベースの使用

---

## 今後の改善予定

- 理想時間配分 UI の実装
- 実績との差分・達成率表示
- レスポンシブ対応
- テストコード追加

---

## 開発チーム

- TechJam Team10

---

## ライセンス

MIT License
