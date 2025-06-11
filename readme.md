# 🛒 Kafka + Spark Streaming - Processamento de Vendas E-commerce

Descrição do Projeto
Este projeto simula o consumo de dados de vendas de um e-commerce utilizando:

* Apache Kafka (mensageria)

* Apache Spark Structured Streaming (processamento em tempo real)

O objetivo é consumir as vendas publicadas no Kafka, processar o JSON recebido, explodir os produtos vendidos e calcular a quantidade total vendida por produto.

# 📦 Tecnologias Utilizadas

* Python 3.x
* Apache Kafka
* Apache Spark (pyspark)
* Kafka-Python (para o producer)
* pyspark.sql (para o consumer)

# 🗄️ Estrutura dos Dados

Cada mensagem no Kafka segue o seguinte schema (em JSON):

{
  "id_ordem": "string",
  "cpf_cliente": "string",
  "produtos_comprados": ["produto1", "produto2"],
  "quantidade_por_produto": { "produto1": 1, "produto2": 2 },
  "valor_total": 1000,
  "data_hora": "2025-06-10T12:34:56"
}

# ⚙️ Como Rodar o Projeto

## 1️⃣ Subir o Kafka

```
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka
bin/kafka-server-start.sh config/server.properties

```
## 2️⃣ Criar o tópico Kafka

```
bin/kafka-topics.sh --create --topic vendas-ecommerce --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

```
## 3️⃣ Rodar o Producer (Gerador de vendas)

```
python produtor_vendas.py

```
## 4️⃣ Rodar o Consumer (Spark Streaming)

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 consumidor_vendas.py

```

# 🚀 Lógica de Processamento

1. Spark lê as mensagens do Kafka no tópico vendas-ecommerce
2. Faz o parsing do JSON recebido.
3. Explode o array de produtos vendidos.
4. Para cada produto, obtém a quantidade vendida.
5. Agrupa por produto e calcula a soma total de cada produto vendido.
6. Exibe os resultados no console.

# 📊 Exemplo de Saída

+----------+----------------+
|produto   |quantidade_total|
+----------+----------------+
|Headset   |25              |
|Mouse     |31              |
|Notebook  |15              |
|Monitor   |7               |
|Impressora|26              |
|Teclado   |33              |
+----------+----------------+

# ✅ Requisitos

* Kafka e Zookeeper rodando
* Spark configurado e funcionando
* Dependências Python instaladas (separar em um requirements.txt se quiser deixar redondo)
