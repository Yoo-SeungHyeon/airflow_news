from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator  # Airflow 2.8.1에서도 사용 가능

def hello():
    print("Hello, Airflow!")

default_args = {
    'start_date': datetime(2024, 1, 1),
    'catchup': False,
}

with DAG(
    dag_id='hello_airflow',
    default_args=default_args,
    description='A simple hello world DAG',
    schedule_interval=None,  # 수동 실행
    tags=['example'],
) as dag:

    task_hello = PythonOperator(
        task_id='say_hello',
        python_callable=hello
    )

    task_hello
