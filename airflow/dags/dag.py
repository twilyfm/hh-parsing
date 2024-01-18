from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from datetime import date
import pendulum
import pandas as pd
from pyspark.sql import SparkSession
import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from data_parsing import parsing
import pandas as pd
from data_parsing import parsing
import os
from datetime import date
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

with DAG(
    dag_id='twilyfm_hh_parsing_dag',
    start_date=pendulum.datetime(2024, 1, 1, tz='UTC'),
    catchup=False,
    schedule_interval='0 0 * * *'
) as dag:

    @task(task_id='twilyfm_data_parsing')
    def get_data(**kwargs):
        vacancy_name = 'Data Science'

        current_date = date.today()

        # parsing hh data
        df = parsing(vacancy_name)

        # start spark session
        spark = SparkSession.builder \
            .master('local[*]') \
            .appName('hh_parsing') \
            .getOrCreate()

        # create spark df
        schema = StructType(
            [
                StructField("name", StringType(), nullable=True),
                StructField("company", StringType(), nullable=True),
                StructField("city", StringType(), nullable=True),
                StructField("salary", StringType(), nullable=True),
                StructField("vacancy_info", StringType(), nullable=True),
                StructField("publication_time", StringType(), nullable=True),
                StructField("description", StringType(), nullable=True),
                StructField("link", StringType(), nullable=True),
            ]
        )

        df_spark = spark.createDataFrame(df, schema=schema)

        # save data into parquet
        df_spark \
            .repartition(1) \
            .write.mode('overwrite') \
            .parquet(f'../data/vacancies_{vacancy_name.replace(" ", "_")}_{current_date}')

    get_data()