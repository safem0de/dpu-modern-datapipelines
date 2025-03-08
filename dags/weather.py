import json
import requests
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from airflow.utils import timezone
from airflow.providers.postgres.hooks.postgres import PostgresHook


DAG_FILE_NAME = "/opt/airflow/dags/data.json"
CONN_STR = "weather_postgres_conn"


def _get_weather_data():
    # assert 1 == 2

    # API_KEY = "7958cef1*********60a3cdfcc3"
    # API_KEY = os.environ.get("WEATHER_API_KEY")
    API_KEY = Variable.get("weather_api_key")

    payload = {
        "q": "bangkok",
        "appid": API_KEY,
        "units": "metric"
    }
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=payload)
    print(response.url)

    data = response.json()
    print(data)

    with open(DAG_FILE_NAME, "w") as f:
        json.dump(data, f)


def _create_weather_table():
    pg_hook = PostgresHook(
        postgres_conn_id=CONN_STR,
        schema="postgres"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS weathers (
            dt BIGINT NOT NULL,
            temp FLOAT NOT NULL,
            feels_like FLOAT NULL
        )
    """

    cursor.execute(sql)
    connection.commit()


def _load_data_to_postgres():
    pg_hook = PostgresHook(
        postgres_conn_id=CONN_STR,
        schema="postgres"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    with open(DAG_FILE_NAME, "r") as f:
        data = json.load(f)

    feels_like = data["main"]["feels_like"]
    temp = data["main"]["temp"]
    dt = data["dt"]

    sql = f"""
        INSERT INTO weathers (dt, temp, feels_like) VALUES ({dt}, {temp}, {feels_like})
    """
    cursor.execute(sql)
    connection.commit()


def _validate_data():
    with open(DAG_FILE_NAME, "r") as f:
        data = json.load(f)

    assert data.get("main") is not None

def _validate_temperature_range():
    with open(DAG_FILE_NAME, "r") as f:
        data = json.load(f)

    assert data.get("main").get("temp") >= 30
    assert data.get("main").get("temp") <= 45


default_args = {
    "email": ["67130503@dpu.ac.th"],
    "retries": 3,
    "relay_delay": timedelta(minutes=1)
}
with DAG(
    "weather_api_dag",
    default_args=default_args,
    schedule="0 */3 * * *",
    start_date=timezone.datetime(2025, 2, 1),
    tags=["dpu"]
):
    start = EmptyOperator(task_id="start")

    get_weather_data = PythonOperator(
        task_id="get_weather_data",
        python_callable=_get_weather_data,
    )

    create_weather_table = PythonOperator(
        task_id="create_weather_table",
        python_callable=_create_weather_table,
    )

    load_data_to_postgres = PythonOperator(
        task_id="load_data_to_postgres",
        python_callable=_load_data_to_postgres,
    )

    validate_data = PythonOperator(
        task_id="validate_data",
        python_callable=_validate_data,
    )

    validate_temperature_range = PythonOperator(
        task_id="validate_temperature_range",
        python_callable=_validate_temperature_range,
    )

    send_email = EmailOperator(
        task_id="send_email",
        to=["kan@odds.team"],
        subject="Finished getting open weather data",
        html_content="Done",
    )

    end = EmptyOperator(task_id="end")


    start >> get_weather_data >> [validate_data, validate_temperature_range] >> load_data_to_postgres >> send_email >> end
    start >> create_weather_table >> load_data_to_postgres >> send_email >>end
