# Databricks notebook source
import pyspark.pandas as ps

# COMMAND ----------

dbutils.fs.ls("dbfs:/databricks-results/bronze/")

# COMMAND ----------

df = ps.read_parquet("dbfs:/databricks-results/bronze/*/*/*")
df.head()


# COMMAND ----------

moedas = ["USD", "EUR", "GBP"]

df_filtrado = df[(df['moeda'] == "USD") | (df['moeda'] == "EUR") | (df['moeda'] == "GBP")]
df_filtrado.head()

# COMMAND ----------

df_filtrado["data"] = ps.to_datetime(df_filtrado["data"])
df_filtrado.dtypes

# COMMAND ----------

df_pivot = df_filtrado.pivot_table(index=["data"], columns="moeda",values="taxa", aggfunc='first').sort_index(ascending=False)
df_pivot.head()

# COMMAND ----------

for moeda in moedas:
    df_pivot[moeda] = df_pivot[moeda].apply(lambda x: round(1 / x, 4))

df_pivot.head()
