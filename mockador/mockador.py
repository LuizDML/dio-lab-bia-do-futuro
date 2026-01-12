import csv
import random
from datetime import datetime, timedelta
import itertools

# Função para gerar datas
def generate_dates(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)

# Categorias e seus estabelecimentos relacionados
estabelecimentos_por_categoria = {
    'moradia': ['Imobiliária Sol Nascente', 'Lar Seguro Imóveis', 'Conforto Lar', 'Casa Nova Imobiliária', 'Morada Feliz'],
    'alimentacao': ['Supermercado Bom Preço', 'Mercado Econômico', 'Hiper Atacado', 'Supreme Supermercados', 'Feira Livre Central'],
    'lazer': ['Cinema Multiplex', 'Netflix', 'Spotify', 'Academia FitPro', 'Parque Aquático', 'Livraria Cultura'],
    'saude': ['Farmácia Popular', 'Drogaria Saúde', 'Clínica Bem Estar', 'Laboratório Diagnóstico', 'Academia Vida Saudável'],
    'transporte': ['Posto Shell', 'Posto Ipiranga', 'Uber', '99 Taxi', 'Metrô', 'Ônibus Municipal'],
    'vestuario': ['Renner', 'C&A', 'Zara', 'H&M', 'Nike', 'Adidas'],
    'educacao': ['Livraria Saraiva', 'Cursos Online Academy', 'Faculdade Digital', 'Editora Moderna'],
    'servicos': ['Barbearia Elite', 'Salão Beauty', 'Assistência Técnica', 'Manutenção Residencial']
}

# Estabelecimentos sem relação (para os 15%)
estabelecimentos_aleatorios = [
    'Padaria Pão Quente', 'Loja de Conveniência', 'Lanchonete Rápida', 
    'Cafeteria Aroma', 'Restaurante Sabor Caseiro', 'Bar do Zé',
    'Pet Shop Amigo Fiel', 'Floricultura Primavera', 'Banca de Jornais',
    'Loja de Eletrônicos', 'Oficina Mecânica', 'Loja de Materiais de Construção'
]

# Métodos de pagamento
metodos_pagamento = ['credito', 'debito', 'pix']

# Função para gerar transações
def generate_transactions():
    transactions = []
    
    # Datas
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    # Receitas (12 salários + 2 parcelas de 13º)
    meses_salario = list(range(1, 13))
    for mes in meses_salario:
        # Salário normal (dia 5 de cada mês)
        data_salario = datetime(2025, mes, 5)
        valor_base = 5000.00
        # Variação de até 10% no salário
        variacao = random.uniform(-0.1, 0.1)
        valor_salario = round(valor_base * (1 + variacao), 2)
        
        transactions.append({
            'data': data_salario.strftime('%Y-%m-%d'),
            'descricao': 'Salário',
            'categoria': 'receita',
            'valor': valor_salario,
            'tipo': 'entrada',
            'estabelecimento': 'Empresa ABC Ltda',
            'metodo_pagamento': 'pix'
        })
    
    # 13º salário (2 parcelas - junho e novembro)
    for mes in [6, 11]:
        data_13 = datetime(2025, mes, 15)
        valor_13 = round(5000.00 / 2, 2)
        transactions.append({
            'data': data_13.strftime('%Y-%m-%d'),
            'descricao': '13º Salário',
            'categoria': 'receita',
            'valor': valor_13,
            'tipo': 'entrada',
            'estabelecimento': 'Empresa ABC Ltda',
            'metodo_pagamento': 'pix'
        })
    
    # Despesas fixas mensais
    despesas_fixas = [
        ('Aluguel', 'moradia', 1200.00),
        ('Condomínio', 'moradia', 350.00),
        ('Plano de Saúde', 'saude', 450.00),
        ('Academia', 'saude', 99.00),
        ('Internet', 'moradia', 120.00),
        ('Celular', 'servicos', 89.90),
        ('Streaming (Netflix+Spotify)', 'lazer', 79.90)
    ]
    
    for mes in range(1, 13):
        for desc, cat, valor in despesas_fixas:
            data_despesa = datetime(2025, mes, random.randint(1, 10))
            transactions.append({
                'data': data_despesa.strftime('%Y-%m-%d'),
                'descricao': desc,
                'categoria': cat,
                'valor': valor,
                'tipo': 'saida',
                'estabelecimento': random.choice(estabelecimentos_por_categoria.get(cat, ['Desconhecido'])),
                'metodo_pagamento': random.choice(metodos_pagamento)
            })
    
    # Despesas variáveis
    categorias_despesas = ['alimentacao', 'transporte', 'lazer', 'vestuario', 'educacao', 'servicos']
    
    for data in generate_dates(start_date, end_date):
        # 70% de chance de ter uma transação no dia (simula pessoa sem controle financeiro)
        if random.random() < 0.7 and data.weekday() not in [5, 6]:  # Menos gastos no fim de semana
            # Pequenos gastos diários
            num_gastos = random.randint(1, 3)
            for _ in range(num_gastos):
                categoria = random.choice(categorias_despesas)
                
                # Decidir se será estabelecimento relacionado ou aleatório (15% aleatório)
                if random.random() < 0.15:
                    estabelecimento = random.choice(estabelecimentos_aleatorios)
                else:
                    estabelecimento = random.choice(estabelecimentos_por_categoria.get(categoria, ['Desconhecido']))
                
                # Valores pequenos para simular falta de controle
                if categoria == 'alimentacao':
                    descricoes = ['Mercado', 'Padaria', 'Lanche', 'Café', 'Almoço', 'Janta']
                    valor = round(random.uniform(8.50, 45.90), 2)
                elif categoria == 'transporte':
                    descricoes = ['Uber', 'Combustível', 'Estacionamento', 'Ônibus', 'Metrô']
                    valor = round(random.uniform(15.00, 85.00), 2)
                elif categoria == 'lazer':
                    descricoes = ['Cinema', 'Bar', 'Restaurante', 'Parque', 'Show']
                    valor = round(random.uniform(25.00, 150.00), 2)
                else:
                    descricoes = [categoria.capitalize()]
                    valor = round(random.uniform(20.00, 120.00), 2)
                
                transactions.append({
                    'data': data.strftime('%Y-%m-%d'),
                    'descricao': random.choice(descricoes),
                    'categoria': categoria,
                    'valor': valor,
                    'tipo': 'saida',
                    'estabelecimento': estabelecimento,
                    'metodo_pagamento': random.choice(metodos_pagamento)
                })
        
        # Gastos maiores esporádicos
        if random.random() < 0.05:  # 5% de chance por dia
            categoria = random.choice(categorias_despesas)
            valor = round(random.uniform(150.00, 800.00), 2)
            descricoes_grandes = ['Compra do Mês', 'Presente', 'Reforma', 'Equipamento', 'Curso']
            
            transactions.append({
                'data': data.strftime('%Y-%m-%d'),
                'descricao': random.choice(descricoes_grandes),
                'categoria': categoria,
                'valor': valor,
                'tipo': 'saida',
                'estabelecimento': random.choice(estabelecimentos_por_categoria.get(categoria, ['Desconhecido'])),
                'metodo_pagamento': random.choice(metodos_pagamento)
            })
    
    # Ordenar por data
    transactions.sort(key=lambda x: x['data'])
    return transactions

# Gerar transações
transacoes = generate_transactions()

# Salvar em CSV
with open('transacoes_2025_completo.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['data', 'descricao', 'categoria', 'valor', 'tipo', 'estabelecimento', 'metodo_pagamento']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for transacao in transacoes:
        writer.writerow(transacao)

print(f"Arquivo 'transacoes_2025_completo.csv' criado com {len(transacoes)} transações.")

# Agora criar o arquivo de gastos recomendados
def create_recommended_spending():
    recomendacoes = [
        {'categoria': 'moradia', 'percentual_recomendado': 30, 'descricao': 'Inclui aluguel/hipoteca, condomínio, IPTU, contas de luz, água, gás, internet'},
        {'categoria': 'alimentacao', 'percentual_recomendado': 15, 'descricao': 'Supermercado, feira, padaria, restaurantes'},
        {'categoria': 'transporte', 'percentual_recomendado': 10, 'descricao': 'Combustível, manutenção do carro, transporte público, aplicativos'},
        {'categoria': 'saude', 'percentual_recomendado': 10, 'descricao': 'Plano de saúde, medicamentos, consultas, academia'},
        {'categoria': 'lazer', 'percentual_recomendado': 10, 'descricao': 'Streaming, cinema, viagens, hobbies, restaurantes'},
        {'categoria': 'vestuario', 'percentual_recomendado': 5, 'descricao': 'Roupas, calçados, acessórios'},
        {'categoria': 'educacao', 'percentual_recomendado': 5, 'descricao': 'Cursos, livros, material de estudo'},
        {'categoria': 'investimentos', 'percentual_recomendado': 15, 'descricao': 'Reserva de emergência, aposentadoria, investimentos'},
        {'categoria': 'outros', 'percentual_recomendado': 10, 'descricao': 'Presentes, doações, despesas imprevistas'}
    ]
    
    with open('gastos_recomendados.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['categoria', 'percentual_recomendado', 'descricao']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for recomendacao in recomendacoes:
            writer.writerow(recomendacao)
    
    print("Arquivo 'gastos_recomendados.csv' criado com recomendações financeiras.")

create_recommended_spending()