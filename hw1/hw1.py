from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
import pandas as pd


conf = SparkConf().setAppName('test3').setMaster("spark://192.168.56.101:7077") 
sc = SparkContext()
sqlContext = SQLContext(sc)

filePath = 'household_power_consumption.csv'
df_pd=pd.read_csv(filePath, sep=';')

df_pd = df_pd.drop(df_pd[df_pd['Global_active_power']  == '?'].index)
# df = df.filter(df.Global_active_power != '?') # for pyspark

print(type(df_pd))
print(df_pd.head())

# df_pd.to_csv('household_power_consumption.csv')
# df_pd=pd.read_csv(filePath, sep=',')

df = sqlContext.createDataFrame(df_pd)
print(type(df))
a = '?'
# remove有?的 row
# df = df.where("Global_active_power != -")
# change dtypes
from pyspark.sql.types import DoubleType

# print(df.dtypes)
# column_list = ['Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity']
column_list = ['Global_active_power']
for column in column_list:
    df = df.withColumn(column, df[column].cast('double'))
df = df[column_list]
df.show(2)
# (1) Output the minimum, maximum, and count of the following columns: ‘global active power’, ‘global reactive power’, ‘voltage’, and ‘global intensity’.
# for column in column_list:
#     df_remove_q.agg({column: 'max'}).show()
#     df_remove_q.agg({column: 'min'}).show()
#     df_remove_q.agg({column: 'count'}).show()
# # (2) Output the mean and standard deviation of these columns.
# df_remove_q.agg({column: 'mean'}).show()
# df_remove_q.agg({column: 'std'}).show()
# (3) Perform min-max normalization on the columns to generate normalized output.

from pyspark.ml.feature import VectorAssembler, StandardScaler, MinMaxScaler

vector_assembler = VectorAssembler(inputCols=column_list, outputCol='ss_features')
temp_train = vector_assembler.transform(df)
temp_train.show(2)

minmax_scaler = MinMaxScaler(inputCol='ss_features', outputCol='scaled')
train = minmax_scaler.fit(temp_train).transform(temp_train)
train.show(2)