# Databricks notebook source
# MAGIC %pip install kaleido slack-sdk

# COMMAND ----------

from slack_sdk import WebClient

# COMMAND ----------

slack_token = "xoxb-6672476962422-6676223855925-5Xk7xuL0bsfoiMTITk2x7wkP"
client = WebClient(token=slack_token)

# COMMAND ----------

nome_arquivo = dbutils.fs.ls("dbfs:/databricks-results/prata//valores_reais/")[-1].name
nome_arquivo

# COMMAND ----------

path = "../../../../dbfs/databricks-results/prata/valores_reais/" + nome_arquivo

# COMMAND ----------

enviando_arquivo_csv = client.files_upload_v2(
    channel="C06KSE5M5B8",
    title="Arquivo no formato CSV do valor do real convertido",
    file=path,
    filename="valores_reais.csv",
    initial_comment="Segue anexo do arquivo CSV:"
)

# COMMAND ----------

import pyspark.pandas as ps

# COMMAND ----------

df_valores_reais = ps.read_csv("dbfs:/databricks-results/prata/valores_reais/")
df_valores_reais.head()

# COMMAND ----------

for moeda in df_valores_reais.columns[1:]:
    fig = df_valores_reais.plot.line(x="data", y=moeda)
    fig.write_image(f"./imagens/{moeda}.png")

# COMMAND ----------

def enviando_imagens(moeda_cotacao):
    enviando_imagens = client.files_upload_v2(
    channel="C06KSE5M5B8",
    title="Imagens de Cotações",
    file=f"./imagens/{moeda_cotacao}.png"
)

# COMMAND ----------

for moeda in df_valores_reais.columns[1:]:
    enviando_imagens(moeda)

# COMMAND ----------


