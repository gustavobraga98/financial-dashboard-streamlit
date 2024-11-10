import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from utils.auth.login import check_password

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Configurar parâmetros de tipo e intervalo
type_param = "outcome"  # ou "income" dependendo do que você quer ver
range_param = "week"  # 'week', 'month', 'year', ou 'all'

response = requests.get(f"{st.secrets['BASEURL']}/dashboard/pizza_graph/?type={type_param}&range={range_param}")

# Verificar o status da resposta antes de processar
if response.status_code == 200:
    data = response.json()

    # Organizar dados para o gráfico de pizza
    category_totals = {category: details["total"] for category, details in data.items()}
    labels = list(category_totals.keys())
    values = list(category_totals.values())

    # Criar gráfico de pizza
    fig = px.pie(values=values, names=labels, title="Despesas por Categoria")

    # Criar as abas usando st.tabs()
    tabs = st.tabs(["Gráfico de Pizza", "Detalhamento das Transações"])

    with tabs[0]:
        # Exibir o gráfico de pizza na primeira aba
        st.plotly_chart(fig)

    with tabs[1]:
        # Exibir transações detalhadas por categoria na segunda aba
        for category, details in data.items():
            st.subheader(category)

            # Criar DataFrame com transações da categoria
            df = pd.DataFrame(details["transactions"])

            # Converter a coluna 'date' para formato de data e 'value' para moeda
            df['date'] = pd.to_datetime(df['date']).dt.date
            df['value'] = df['value'].apply(lambda x: f"R$ {x:,.2f}")

            # Exibir a tabela de transações com pandas
            st.dataframe(df)

else:
    st.error("Erro ao buscar dados para o gráfico de pizza.")
