FROM apache/airflow:2.10.5

USER root

# Java 설치
RUN apt update && apt install -y default-jdk

# 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# airflow 사용자로 전환
USER airflow

# pip 패키지 설치 (airflow 사용자로 실행해야 함)
RUN pip install --no-cache-dir konlpy beautifulsoup4 requests psycopg2-binary
