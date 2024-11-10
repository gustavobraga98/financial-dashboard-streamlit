import streamlit as st
import requests
import pandas as pd
from utils.auth.login import check_password

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

def send_transaction():
    # Substitui "Outra..." pela nova categoria, se ela tiver sido preenchida
    final_category = st.session_state["new_category"] if st.session_state["category"] == "Outra..." and st.session_state["new_category"] else st.session_state["category"]
    
    date_str = st.session_state["date"].isoformat()
    
    response = requests.post(
        f'{st.secrets["BASEURL"]}/transactions/',
        json={
            "type": st.session_state["transaction_type"],
            "value": st.session_state["value"],
            "description": st.session_state["description"],
            "category": final_category,
            "date": date_str
        }
    )
    if response.status_code == 200:
        st.success("Transação adicionada com sucesso!")
    else:
        st.error(f"Erro ao adicionar transação: {response.text}")

st.set_page_config(
    page_title="Transactions",
    page_icon="👋",
)

st.write("# Transactions")

# Inputs armazenados no st.session_state
st.selectbox(
    "Selecione o tipo de transação:",
    options=["income", "outcome"],
    index=0,
    key="transaction_type"
)

st.number_input("Insira o valor:", key="value")
st.text_input("Insira a descrição:", key="description")

categories = requests.get(f'{st.secrets["BASEURL"]}/categories/').json()
categories.append("Outra...")

st.selectbox("Selecione ou insira a categoria:", options=categories, key="category")

# Campo de texto para nova categoria, exibido apenas se "Outra..." for selecionada
if st.session_state["category"] == "Outra...":
    st.text_input("Insira a nova categoria:", key="new_category")

st.date_input("Insira a data:", key="date")

# Botão que chama a função send_transaction
st.button("Adicionar transação", on_click=send_transaction)
