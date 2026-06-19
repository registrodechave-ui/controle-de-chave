import streamlit as st
from auth import verificar_login

from database import (
    listar_chaves_disponiveis,
    listar_motoristas,
    registrar_saida
)

verificar_login()

st.title("🔑 Retirada de Chaves")

if st.session_state.get("limpar_retirada", False):
    st.session_state["numero_chave_retirada"] = ""
    st.session_state["matricula_retirada"] = ""
    st.session_state["limpar_retirada"] = False

chaves = listar_chaves_disponiveis()
motoristas = listar_motoristas()

if not chaves:
    st.warning("Nenhuma chave disponível.")
    st.stop()

if not motoristas:
    st.warning("Nenhum motorista cadastrado.")
    st.stop()

opcoes_chaves = {
    str(item["chave"]): item
    for item in chaves
}

opcoes_motoristas = {
    str(m["matricula"]): m
    for m in motoristas
}

numero_chave = st.text_input(
    "Digite o número da chave",
    key="numero_chave_retirada"
)

dados_chave = None

if numero_chave.strip():
    dados_chave = opcoes_chaves.get(numero_chave.strip())

    if not dados_chave:
        st.warning("Chave não encontrada ou não disponível.")

st.text_input(
    "Tipo do Veículo",
    value=dados_chave["tp_carro"] if dados_chave else "",
    disabled=True
)

matricula = st.text_input(
    "Digite a matrícula do motorista",
    key="matricula_retirada"
)

motorista = None

if matricula.strip():
    motorista = opcoes_motoristas.get(matricula.strip())

    if not motorista:
        st.warning("Motorista não encontrado.")

st.text_input(
    "Nome do Motorista",
    value=motorista["nome"] if motorista else "",
    disabled=True
)

stv = st.checkbox(
    "STV - Setor de Veiculos"
)

if st.button(
    "Registrar Retirada",
    type="primary",
    use_container_width=True
):

    if not numero_chave.strip():
        st.warning("Informe o número da chave.")
        st.stop()

    if not dados_chave:
        st.warning("Chave não encontrada ou não disponível.")
        st.stop()

    if not matricula.strip():
        st.warning("Informe a matrícula do motorista.")
        st.stop()

    if not motorista:
        st.warning("Motorista não encontrado.")
        st.stop()

    status = "STV" if stv else "Aberto"
    tipo_saida = "STV" if stv else "Normal"

    try:
        registrar_saida(
            chave=dados_chave["chave"],
            tp_carro=dados_chave["tp_carro"],
            matricula=motorista["matricula"],
            nome=motorista["nome"],
            usuario_logado=st.session_state["usuario"],
            status=status,
            tipo_saida=tipo_saida
        )

        st.success("Retirada registrada com sucesso!")

        st.session_state["limpar_retirada"] = True
        st.rerun()

    except Exception as erro:
        st.error(str(erro))