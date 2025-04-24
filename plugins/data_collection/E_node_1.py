import json
import requests
from dotenv import load_dotenv
import os
from typing import List, Dict
import psycopg2

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
db_url = os.getenv("POSTGRES_URL")




def get_news_list(query: str, display: int, start: int, sort: str) -> None:
    '''
    query : 검색어 (UTF-8 인코딩 필수)
    display : 한 번에 표시할 검색 결과 개수 (10 ~ 100)
    start : 검색 시작 위치 (1 ~ 1000)
    sort : 검색 결과 정렬 방법 ('sim'=정확도 내림차순, 'date'=날짜 내림차순)
    '''
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
    return response.json()['items']

def save_staging(items: List[Dict]):
    '''
    뉴스 데이터를 PostgreSQL staging 테이블에 저장
    '''
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS news_staging (
        id SERIAL PRIMARY KEY,
        title TEXT,
        pub_date TEXT,
        originallink TEXT,
        description TEXT
    );
    """
    cur.execute(create_table_query)

    insert_query = """
    INSERT INTO news_staging (title, pub_date, originallink, description)
    VALUES (%s, %s, %s, %s);
    """
    for item in items:
        cur.execute(insert_query, (
            item.get("title"),
            item.get("pubDate"),
            item.get("originallink"),
            item.get("description")
        ))

    conn.commit()
    cur.close()
    conn.close()



if __name__ == "__main__":
    items = get_news_list("삼성전자", 100, 1, 'date')
    print(items)
    save_staging(items)