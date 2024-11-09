import streamlit as st
import requests
import pandas as pd
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

st.set_page_config(
    page_title="Home",
    page_icon="📈",
)

st.write("# Dashboard Financeiro 📈")

st.write("## Gastos do mês")
monthly_report = requests.get(st.secrets["BASEURL"] + "/home/monthly-expenses/").json()
monthly_report_cols = st.columns(8)
with monthly_report_cols[0]:
    st.write(f":red[{monthly_report['total_expenses']}]")

with monthly_report_cols[7]:
    st.write(monthly_report['total_income'])
st.progress(monthly_report["total_percentage"])


st.divider()

st.write(f"### Balanço do saldo")

# Seletor para escolher o intervalo de tempo
time_range = st.selectbox(
    "Selecione o intervalo de tempo:",
    options=["week", "month", "year"],
    index=0  # Inicia com "week"
)

# Função para atualizar o saldo e o gráfico
def update_balance(time_range):
    with st.spinner("Carregando..."):
        # Chama a API para obter o saldo acumulado por período
        response = requests.get(f'{st.secrets["BASEURL"]}/home/balance/?range={time_range}')
        balance_data = response.json()
        # Cria um DataFrame a partir do dicionário de resposta
        balance_df = pd.DataFrame(list(balance_data.items()), columns=['date', 'value'])


        # Converte a coluna 'date' para datetime automaticamente
        balance_df['date'] = pd.to_datetime(balance_df['date'], errors='coerce')


        # Remove qualquer linha que tenha valores NaT (caso a conversão falhe em alguma linha)
        balance_df = balance_df.dropna(subset=['date'])


        # Define a coluna 'date' como o índice do DataFrame
        balance_df.set_index('date', inplace=True)

        # Ordena o DataFrame por data
        balance_df.sort_index(inplace=True)

        # Exibe o gráfico com base no intervalo selecionado
        if time_range == "week":
            st.line_chart(balance_df['value'])
        elif time_range == "month":
            st.line_chart(balance_df['value'])
        elif time_range == "year":
            st.line_chart(balance_df['value'])

# Chama a função para atualizar o saldo quando o seletor muda
update_balance(time_range)
