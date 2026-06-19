import streamlit as st
import pandas as pd

from database import listar_chaves_abertas
from auth import verificar_login

verificar_login()

st.title("🔓 Chaves em Aberto")

dados = listar_chaves_abertas()

if not dados:
    st.success("Nenhuma chave em aberto.")
else:

    df = pd.DataFrame(dados)

    colunas = [
        "chave",
        "tp_carro",
        "matricula",
        "nome",
        "status",
        "data_saida"
    ]

    df = df[colunas]

    if "data_saida" in df.columns:
        df["data_saida"] = pd.to_datetime(
            df["data_saida"],
            errors="coerce"
        ).dt.strftime("%d/%m/%Y %H:%M:%S")

    df = df.rename(columns={
        "chave": "Chave",
        "tp_carro": "Veículo",
        "matricula": "Matrícula",
        "nome": "Motorista",
        "status": "Status",
        "data_saida": "Data Saída"
    })

    busca = st.text_input(
        "🔍 Buscar por chave, veículo, matrícula, motorista ou status"
    )

    if busca.strip():

        busca = busca.strip().lower()

        df = df[
            df.astype(str)
            .apply(
                lambda linha: linha.str.lower().str.contains(busca).any(),
                axis=1
            )
        ]

    st.dataframe(
        df,
        use_container_width=True
    )