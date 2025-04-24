from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="news_etl",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["demo"]
) as dag:

    extract_news = BashOperator(
        task_id="run_e_node",
        bash_command="python /opt/airflow/plugins/data_collection/E_node.py"
    )

    transform_keywords = BashOperator(
        task_id="run_t_node",
        bash_command="python /opt/airflow/plugins/data_collection/T_node.py"
    )

    extract_news >> transform_keywords
