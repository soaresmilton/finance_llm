import os
from dotenv import load_dotenv, find_dotenv
from df_transactions import df_transactions
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

## Tratativa dos dados com LLM:
load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

template = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados.
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar.

Todos são transações financeiras de uma pessoa física.

Escolha uma dentre as seguintes categorias:
- Alimentação
- Receitas
- Saúde
- Mercado
- Saúde
- Educação
- Compras
- Transporte
- Investimento
- Transferências para terceiros
- Telefone
- Moradia

Classifique o item em uma das categorias mencionadas:
{text}

Responda apenas com a categoria.
"""

prompt = PromptTemplate.from_template(template=template)

model_name = 'llama-3.1-8b-instant' #os.getenv('MODEL', 'mixtral-8x7b-32768') # "llama-3.1-70b-versatile" 'llama-3.1-8b-instant' groq_api_key=GROQ_API_KEY,

chat = ChatGroq(groq_api_key=GROQ_API_KEY, model=model_name)
chain = prompt | chat | StrOutputParser()

categorias = chain.batch(list(df_transactions["Descrição"].values))
df_transactions["Categorias"] = categorias

df = df[df_transactions["Data"] >= datetime(2024, 3, 1).date()]
df.to_csv("finances.csv")