from kafka import KafkaProducer
import json
import uuid
from faker import Faker
import random
from datetime import datetime

fake = Faker('pt_BR')  # Para dados no padrão brasileiro

# Configura o produtor Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Lista de produtos disponíveis no e-commerce
produtos_disponiveis = ['Teclado', 'Notebook', 'Headset', 'Monitor', 'Mouse', 'Impressora']

def gerar_venda():
    id_ordem = str(uuid.uuid4())
    cpf_cliente = fake.cpf()
    
    # Seleciona aleatoriamente 1 a 4 produtos diferentes para a venda
    produtos_comprados = random.sample(produtos_disponiveis, random.randint(1, 4))
    
    quantidade_por_produto = {}
    valor_total = 0
    
    for produto in produtos_comprados:
        quantidade = random.randint(1, 5)  # Quantidade de 1 a 5
        quantidade_por_produto[produto] = quantidade
        
        # Simula preço para cada produto (exemplo simples)
        preco_unitario = random.randint(100, 5000)
        valor_total += preco_unitario * quantidade
    
    data_hora = fake.date_time_this_year().strftime('%d/%m/%Y %H:%M:%S')
    
    venda = {
        'id_ordem': id_ordem,
        'cpf_cliente': cpf_cliente,
        'produtos_comprados': produtos_comprados,
        'quantidade_por_produto': quantidade_por_produto,
        'valor_total': valor_total,
        'data_hora': data_hora
    }
    
    return venda

# Envia 5 vendas como exemplo
for _ in range(5):
    venda = gerar_venda()
    print(f"Enviando venda: {venda}")
    producer.send('vendas-ecommerce', venda)

producer.flush()  # Garante que todas mensagens foram enviadas

