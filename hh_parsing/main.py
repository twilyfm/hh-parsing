import pandas as pd

from config import vacancy_name
from data_parsing import parsing
import os
from datetime import date
from pyspark.sql import SparkSession

current_date = date.today()

# create directory for fata
# if not os.path.exists('./data'):
#     os.mkdir('./data')

# parsing hh data
# df = parsing(vacancy_name)

# df.to_csv('../data/hh_parsing.csv')

df = pd.read_csv('../data/hh_parsing.csv')
# run spark
spark = SparkSession.builder\
    .master('local[*]')\
    .appName('hh_parsing')\
    .getOrCreate()

# create spark dataframe
df_spark = spark.createDataFrame(df)

# save data into parquet
df_spark.repartition(1).write.mode('overwrite').parquet(f'data/vacancies_{current_date}')