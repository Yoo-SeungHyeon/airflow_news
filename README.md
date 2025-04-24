
초기 세팅 (처음 Airflow 세팅할 때)
```bash
# 처음 Airflow를 Docker Compose로 세팅한다면 실행
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml'
# Docker Compose가 존재한다면
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up
```


종료
```bash
docker compose down --volumes --rmi all
```



재시작
```bash
docker compose down --volumes
docker compose build
docker compose up -d
```


postgresql 컨테이너 접속
```bash
docker exec -it airflow_news-postgres-1 psql -U airflow -d airflow
```

db 확인
```bash
SELECT COUNT(*) FROM news_staging;
SELECT * FROM news_staging LIMIT 20;
SELECT COUNT(*) FROM keyword_freq;
SELECT * FROM keyword_freq LIMIT 20;
```