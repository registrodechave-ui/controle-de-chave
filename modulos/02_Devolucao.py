import streamlit as st
from auth import verificar_login

from database import (
    listar_chaves_para_devolucao,
    listar_motoristas,
    registrar_devolucao
)

verificar_login()

st.title("🔄 Devolução de Chaves")

if st.session_state.get("limpar_devolucao", False):
    st.session_state["numero_chave_devolucao"] = ""
    st.session_state["matricula_devolucao"] = ""
    st.session_state["limpar_devolucao"] = False

dados = listar_chaves_para_devolucao()

if not dados:
    st.success("Nenhuma chave em aberto.")
    st.stop()

motoristas = listar_motoristas()

opcoes_chaves = {
    str(item["chave"]).strip().upper(): item
    for item in dados
}

opcoes_motoristas = {
    str(m["matricula"]): m
    for m in motoristas
}

numero_chave = st.text_input(
    "Digite o número da chave",
    key="numero_chave_devolucao"
)

registro = None

if numero_chave.strip():

    registro = opcoes_chaves.get(
        numero_chave.strip().upper()
    )

    if not registro:
        st.warning(
            "Chave não encontrada ou não está em aberto."
        )

st.text_input(
    "Veículo",
    value=registro["tp_carro"] if registro else "",
    disabled=True
)

st.text_input(
    "Motorista da Retirada",
    value=registro["nome"] if registro else "",
    disabled=True
)

matricula_dev = st.text_input(
    "Matrícula Devolução",
    key="matricula_devolucao"
)

motorista_dev = None

if matricula_dev.strip():

    motorista_dev = opcoes_motoristas.get(
        matricula_dev.strip()
    )

    if not motorista_dev:
        st.warning(
            "Motorista não encontrado."
        )

st.text_input(
    "Nome Devolução",
    value=motorista_dev["nome"] if motorista_dev else "",
    disabled=True
)

if st.button(
    "Registrar Devolução",
    type="primary",
    use_container_width=True
):

    if not numero_chave.strip():
        st.warning(
            "Informe o número da chave."
        )
        st.stop()

    if not registro:
        st.warning(
            "Chave não encontrada ou não está em aberto."
        )
        st.stop()

    if not matricula_dev.strip():
        st.warning(
            "Informe a matrícula de quem está devolvendo."
        )
        st.stop()

    if not motorista_dev:
        st.warning(
            "Motorista não encontrado."
        )
        st.stop()

    try:

        registrar_devolucao(
            chave=registro["chave"],
            matricula_dev=matricula_dev,
            nome_dev=motorista_dev["nome"],
            usuario_logado=st.session_state["usuario"]
        )

        st.success(
            "Devolução registrada com sucesso!"
        )

        st.session_state["limpar_devolucao"] = True
        st.rerun()

    except Exception as erro:
        st.error(str(erro))