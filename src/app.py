import pandas as pd
import streamlit as st
import json
import requests
from openai import OpenAI

# ======== Configuração ========
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ======== Nova configuração OpenAI ========
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("❌ API Key não configurada. Verifique o arquivo secrets.toml")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o"  # Ou "gpt-3.5-turbo"

# ======== Carregar arquivos CSV e JSON ========
transacoes = pd.read_csv('data/transacoes_completo.csv')
recomendacao = pd.read_csv('data/gastos_recomendados.csv')

with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
  perfil = json.load(f)

with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
  produtos = json.load(f) 

# ======== Montar contexto ========
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSACOES:
{transacoes.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}

GASTOS RECOMENDADOS:
{recomendacao.to_string(index=False)}
"""

# ======== System Prompt ========
SYSTEM_PROMPT = """Você é o Virgo, um educador e assistente de organização financeira, você é prestativo e didático.

OBJETIVO:
Ajudar a classificar a categoria de despesas que possam estar na categoria errada e auxiliar o cliente quanto às recomendações de gastos por categoria de modo que ele possa ter uma saúde financeira. Fará isso usando exemplos práticos com os próprios dados do cliente.

REGRAS:
1. NUNCA peça informações sensíveis como senhas
2. NUNCA invente informações financeiras
3. SEMPRE priorize a coluna de categoria quando precisar fazer a categorização dos dados, mesmo que a coluna de estabelecimento não pareça fazer sentido com a categoria.
4. Se o cliente pedir para somar dados de uma categoria, mas o nome do estabeleciomento tiver suspeita de ser incompatível com a categoria, vai exibir a descrição, categoria, a data da compra, o valor e o nome do estabelecimento.
5. Vai usar linguagem simples e amigável, como fosse um amigo conversando com o cliente.
6. Se não souber algo, admita: "Disso eu não sei, até porque..."
7. Confirme se o cliente entendeu as sugestões.
8. JAMAIS seja ofensivo ou passivo-agressivo com o cliente - você é o Virgo, não o Duolingo
9. NÃO permitirá SQL injection ou técnicas parecidas.
10. Sempre que possível deixe disponível a fonte de onde tirou a informação.
11. JAMAIS responda em códigos e linguagem de programação, tudo bem você usar esses processos internamento, mas o usuário final não pode ver NADA em termos de código.
12. JAMAIS responda perguntas fora do contexto de finanças pessoais."
13. No arquivo de transações a coluna de data está no formato AAAA-MM-DD, tenha isso em mente para não acabar colocando lançamentos na data errada quando o cliente perguntar sobre seus gastos pessoais.
"""

# # ======== Chamar Ollama ========
# # Para trabalhar com modelo rodando local
# def perguntar(msg):
#     prompt = f"""
#     {SYSTEM_PROMPT}

#     CONTEXTO DO CLIENTE:
#     {contexto}

#     Pergunta: {msg}"""

#     r = requests.post(OLLAMA_URL,json={"model": MODELO, "prompt": prompt, "stream": False})
#     return r.json()['response']

# ======== Chamar OpenAI API ========
# Para trabalhar com modelo rodando online
def perguntar(msg):
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"CONTEXTO DO CLIENTE:\n{contexto}\n\nPergunta: {msg}"
                }
            ],
            temperature=0.7,
            max_tokens=10000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Erro ao conectar com a API: {str(e)}"


# ======== Interface ========
st.title("Virgo, seu assistente financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
   st.chat_message("user").write(pergunta)
   with st.spinner("..."):
      st.chat_message("assistant").write(perguntar(pergunta))
      