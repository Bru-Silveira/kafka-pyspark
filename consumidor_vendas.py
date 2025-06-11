from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, expr, sum as spark_sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, MapType, ArrayType

# Inicializa SparkSession com suporte a Kafka
spark = SparkSession.builder \
    .appName("KafkaConsumerPySpark") \
    .getOrCreate()

# Schema para o JSON das vendas
schema = StructType([
    StructField("id_ordem", StringType(), True),
    StructField("cpf_cliente", StringType(), True),
    StructField("produtos_comprados", ArrayType(StringType()), True),
    StructField("quantidade_por_produto", MapType(StringType(), IntegerType()), True),
    StructField("valor_total", IntegerType(), True),
    StructField("data_hora", StringType(), True)
])

# Lê do tópico Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "vendas-ecommerce") \
    .option("startingOffsets", "earliest") \
    .load()

# Kafka traz os dados no campo 'value' em bytes, convertemos para string
df_string = df.selectExpr("CAST(value AS STRING) as json_str")

# Parseia o JSON da mensagem com o schema
df_json = df_string.select(from_json(col("json_str"), schema).alias("data")).select("data.*")

# # AQUI ENTRA O DEBUG:
# query_debug = df_json.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .start()

# query_debug.awaitTermination()

# Explode produtos para transformar array em linhas
df_exploded = df_json.select(
    col("id_ordem"),
    col("cpf_cliente"),
    explode(col("produtos_comprados")).alias("produto"),
    col("quantidade_por_produto"),
    col("valor_total"),
    col("data_hora")
)

# Para cada produto, pega a quantidade correspondente
df_produtos_qtd = df_exploded.withColumn("quantidade", col("quantidade_por_produto").getItem(col("produto")))

# Agrupa por produto e soma o valor total proporcional à quantidade vendida do produto
# Como valor_total é da venda inteira, aqui simplificamos somando valor_total * quantidade do produto / total de quantidade da venda
# Para simplificar, só somamos quantidade vendida por produto (exemplo básico)
df_agrupado = df_produtos_qtd.groupBy("produto").agg(
    spark_sum("quantidade").alias("quantidade_total")
)

print("Iniciando o streaming de leitura do Kafka...")
# Mostra no console
query = df_agrupado.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

print("Streaming iniciado, aguardando dados...")
query.awaitTermination()
