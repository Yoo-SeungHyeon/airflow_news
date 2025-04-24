import psycopg2
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import defaultdict
from dotenv import load_dotenv
import os
import re

# .env 로드
load_dotenv()
DB_URL = os.getenv("POSTGRES_URL", "postgresql://airflow:airflow@postgres:5432/airflow")

# 형태소 분석기
okt = Okt()

# DB 연결
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# ✅ 테이블 자동 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS keyword_freq (
    id SERIAL PRIMARY KEY,
    pub_date TEXT,
    keyword TEXT,
    count INTEGER
)
""")
conn.commit()

# 뉴스 URL 불러오기
cursor.execute("SELECT pub_date, originallink FROM news_staging")
rows = cursor.fetchall()

# 날짜별 키워드 카운트 딕셔너리
keyword_count = defaultdict(lambda: defaultdict(int))

# 본문 추출 함수 (3자 이상 한글 포함)
def extract_meaningful_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    texts = []

    for tag in soup.find_all():
        text = tag.get_text().strip()
        if len(text) < 10:
            continue
        if re.search(r"[가-힣]{3,}", text):
            texts.append(text)

    return " ".join(texts)

# 본문 크롤링 및 명사 추출
for pub_date, url in rows:
    try:
        html = requests.get(url, timeout=3).text
        text = extract_meaningful_text(html)
        nouns = okt.nouns(text)

        for noun in nouns:
            keyword_count[pub_date][noun] += 1

    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}")
        continue

# 결과 출력 + DB 저장
print("\n✅ 저장 시작")
for date, keywords in keyword_count.items():
    for word, count in keywords.items():
        cursor.execute(
            "INSERT INTO keyword_freq (pub_date, keyword, count) VALUES (%s, %s, %s)",
            (date, word, count)
        )

conn.commit()
conn.close()
print("✅ 저장 완료")
