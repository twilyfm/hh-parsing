import pandas as pd
from config import vacancy_name
from data_parsing import parsing
import os
from datetime import date
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

current_date = date.today()

# parsing hh data
df = parsing(vacancy_name)

# start spark session
spark = SparkSession.builder\
    .master('local[*]')\
    .appName('hh_parsing')\
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
df_spark\
    .repartition(1)\
    .write.mode('overwrite')\
    .parquet(f'../data/vacancies_{vacancy_name.replace(" ", "_")}_{current_date}')
