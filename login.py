import streamlit as st
from database import autenticar_usuario

def tela_login():

    st.title("🔐 Login")

    usuario = st.text_input("Usuário")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button(
        "Entrar",
        use_container_width=True
    ):

        dados = autenticar_usuario(
            usuario,
            senha
        )

        if dados:

            st.session_state["logado"] = True
            st.session_state["usuario"] = dados["username"]
            st.session_state["nivel"] = dados["nivel"]

            st.rerun()

        else:
            st.error(
                "Usuário ou senha inválidos."
            )