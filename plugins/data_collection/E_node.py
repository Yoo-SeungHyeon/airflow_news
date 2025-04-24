import json
import requests
from dotenv import load_dotenv
import os
from typing import List, Dict
import psycopg2

# 환경 변수 로드
load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
db_url = os.getenv("POSTGRES_URL", "postgresql://airflow:airflow@postgres:5432/airflow")


def get_news_list(query: str, display: int, start: int, sort: str) -> List[Dict]:
    url = "https://openapi.naver.com/v1/search/news.json"
    params = {
        "query": query,
        "display": display,
        "start": start,
        "sort": sort
    }
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print("❌ API 호출 실패:", response.text)
        return []

    data = response.json()
    if 'items' not in data:
        print("❌ 'items' 키가 응답에 없음:", data)
        return []

    return data['items']


def save_staging(items: List[Dict]):
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS news_staging (
        id SERIAL PRIMARY KEY,
        title TEXT,
        pub_date TEXT,
        originallink TEXT UNIQUE,
        description TEXT
    );
    """
    cur.execute(create_table_query)
    conn.commit()

    insert_query = """
    INSERT INTO news_staging (title, pub_date, originallink, description)
    SELECT %s, %s, %s, %s
    WHERE NOT EXISTS (
        SELECT 1 FROM news_staging WHERE originallink = %s
    );
    """

    for item in items:
        cur.execute(insert_query, (
            item.get("title"),
            item.get("pubDate"),
            item.get("originallink"),
            item.get("description"),
            item.get("originallink")
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    items = get_news_list("삼성전자", 100, 1, 'date')
    print(items)
    save_staging(items)
