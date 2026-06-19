import streamlit as st

def verificar_login():

    if not st.session_state.get("logado", False):
        st.stop()


def verificar_admin():

    verificar_login()

    if st.session_state.get("nivel") != "admin":
        st.stop()


def usuario_admin():

    return st.session_state.get("nivel") == "admin"