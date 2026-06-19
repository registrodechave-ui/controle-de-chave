import streamlit as st
import pandas as pd
import runpy
from login import tela_login
from datetime import datetime
from auth import usuario_admin

from database import (
    listar_chaves,
    listar_motoristas,
    listar_chaves_abertas,
    listar_registros
)

st.set_page_config(
    page_title="Sistema de Chaves",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    tela_login()
    st.stop()

st.sidebar.title("🔑 Sistema de Chaves")

st.sidebar.write(
    f"👤 Usuário: {st.session_state.get('usuario', '')}"
)

st.sidebar.write(
    f"🔐 Perfil: {st.session_state.get('nivel', '').capitalize()}"
)

st.sidebar.divider()

opcoes_menu = [
    "Início",
    "Retirada",
    "Devolução",
    "Chaves Abertas",
]

if usuario_admin():
    opcoes_menu.insert(4, "Cadastros")
    opcoes_menu.insert(5, "Relatórios")

pagina = st.sidebar.radio(
    "Menu",
    opcoes_menu
)

if st.sidebar.button("🚪 Sair"):
    st.session_state.clear()
    st.rerun()

if pagina == "Início":

    st.title("🔑 Sistema de Controle de Chaves")

    chaves = listar_chaves()
    motoristas = listar_motoristas()
    abertas = listar_chaves_abertas()
    registros = listar_registros()
    stv = len([
        item
        for item in abertas
        if item["status"] == "STV"
    ])

    em_uso = len([
        item
        for item in abertas
        if item["status"] == "Aberto"
    ])

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "🔑 Total de Chaves",
            len(chaves)
        )

    with col2:
        st.metric(
            "🟢 Disponíveis",
            len(chaves) - len(abertas)
        )

    with col3:
        st.metric(
            "🔴 Em Uso",
            len(abertas)
        )

    with col4:
        st.metric(
            "🟡 STV",
            stv
        )

    with col5:
        st.metric(
            "👤 Motoristas",
            len(motoristas)
        )

    st.divider()

    st.subheader("🔓 Chaves em Uso")

    if abertas:

        tabela = []

        def calcular_tempo_uso(data_saida):

            data = pd.to_datetime(
                data_saida,
                errors="coerce"
            )

            if pd.isna(data):
                return ""

            diferenca = datetime.now() - data.to_pydatetime()

            dias = diferenca.days
            horas = diferenca.seconds // 3600
            minutos = (diferenca.seconds % 3600) // 60

            if dias > 0:
                return f"{dias}d {horas}h {minutos}min"

            if horas > 0:
                return f"{horas}h {minutos}min"

            return f"{minutos}min"

        for item in abertas:
            tabela.append({
                "Chave": item["chave"],
                "Veículo": item["tp_carro"],
                "Matricula": item["matricula"],
                "Motorista": item["nome"],
                "status": item["status"],
                "Data Saída": item["data_saida"],
                "Tempo em Uso": calcular_tempo_uso(item["data_saida"])
            })
            
        df_abertas = pd.DataFrame(tabela)

        df_abertas["Data Saída"] = pd.to_datetime(
            df_abertas["Data Saída"],
            errors="coerce"
        ).dt.strftime("%d/%m/%Y %H:%M:%S")

        df_abertas = df_abertas.sort_values(
            by="Data Saída"
        )

        st.dataframe(
            df_abertas,
            use_container_width=True
        )

    else:
        st.success(
            "Nenhuma chave em uso."
        )

elif pagina == "Retirada":
    runpy.run_path("modulos/01_Retirada.py")

elif pagina == "Devolução":
    runpy.run_path("modulos/02_Devolucao.py")

elif pagina == "Chaves Abertas":
    runpy.run_path("modulos/03_Chaves_Abertas.py")

elif pagina == "Cadastros":
    runpy.run_path("modulos/04_Cadastros.py")

elif pagina == "Relatórios":
    runpy.run_path("modulos/05_Relatorios.py")