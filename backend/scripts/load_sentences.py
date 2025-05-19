# scripts/load_sentences.py

import csv
import sys
import os
import django
from pathlib import Path
import argparse

# Djangoセットアップ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from englishbattle.models import Book, Sentence

# ✅ 引数処理
parser = argparse.ArgumentParser(description="CSVからSentenceを読み込む")
parser.add_argument("--title", required=True, help="対象のBookタイトル")
parser.add_argument("--file", default="scripts/data/sentence.csv", help="CSVファイルのパス")
args = parser.parse_args()

book_title = args.title
csv_path = Path(args.file)

# ✅ Book取得
try:
    book = Book.objects.get(title=book_title)
except Book.DoesNotExist:
    print(f"❌ Bookが見つかりません: {book_title}")
    sys.exit(1)

# ✅ CSV読み込み・登録
with open(csv_path, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        number = row.get("Number", "").strip()
        japanese = row.get("Japanese", "").strip()
        english = row.get("English", "").strip()

        if not japanese or not english:
            continue

        try:
            number = int(number)
        except ValueError:
            print(f"スキップ（番号不正）: '{row}'")
            continue

        obj, created = Sentence.objects.get_or_create(
            book=book,
            number=number,
            defaults={"japanese": japanese, "english": english},
        )

        if created:
            print(f"✅ 追加: {obj}")
        else:
            print(f"⚠️ 既に存在: {obj}")
