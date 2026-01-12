# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `transacoes_completo.csv` | CSV | Analisar padrão de gastos do cliente |
| `gastos_recomendados.csv` | CSV | Padrão saudável de gastos por categoria em porcentagem |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Modificado arquivo transacoes.csv para transacoes_completo.csv com dados do período de um ano (01/01/25 a 31/12/25), adicionando novas colunas para o estabeleciomento e tipo de pagamento.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

```python
import pandas as pd
import json

transacoes = pd.read_csv('data/transacoes_completo.csv')
recomendacao = pd.read_csv('data/gastos_recomendados.csv')

with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
  perfil = json.load(f)

with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
  produtos = json.load(f) 
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Dados injetados no system prompt

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
