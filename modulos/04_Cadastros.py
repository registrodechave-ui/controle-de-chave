import streamlit as st
from auth import verificar_admin

from database import (
    cadastrar_chave,
    cadastrar_motorista,
    cadastrar_usuario,

    buscar_chave_por_id,
    atualizar_chave,
    excluir_chave,

    buscar_motorista_por_id,
    atualizar_motorista,
    excluir_motorista,

    buscar_usuario_por_id,
    atualizar_usuario,
    inativar_usuario,
    ativar_usuario,

    listar_chaves,
    listar_motoristas,
    listar_usuarios
)

verificar_admin()

st.title("⚙️ Cadastros")

if "editar_chave_id" not in st.session_state:
    st.session_state["editar_chave_id"] = None

if "editar_motorista_id" not in st.session_state:
    st.session_state["editar_motorista_id"] = None

if "editar_usuario_id" not in st.session_state:
    st.session_state["editar_usuario_id"] = None

aba1, aba2, aba3 = st.tabs(
    [
        "🔑 Chaves",
        "👤 Motoristas",
        "👥 Usuários"
    ]
)

# ==================================
# CHAVES
# ==================================

with aba1:

    st.subheader("Cadastrar Chave")

    chave = st.text_input(
        "Número da Chave",
        key="nova_chave"
    )

    tp_carro = st.text_input(
        "Tipo do Veículo",
        key="novo_tipo"
    )

    if st.button(
        "Salvar Chave",
        use_container_width=True
    ):
        
        if not chave.strip() or not tp_carro.strip():
            st.warning("Preencha todos os campos da chave.")
            st.stop()

        try:

            cadastrar_chave(
                chave,
                tp_carro
            )

            st.success(
                "Chave cadastrada!"
            )

            st.rerun()

        except Exception as erro:
            st.error(str(erro))

    st.divider()

    # ==========================
    # EDIÇÃO
    # ==========================

    if st.session_state["editar_chave_id"]:

        chave_edit = buscar_chave_por_id(
            st.session_state["editar_chave_id"]
        )

        if chave_edit:

            st.warning("Modo edição")

            nova_chave = st.text_input(
                "Número da Chave",
                value=chave_edit["chave"],
                key="edit_chave"
            )

            novo_tipo = st.text_input(
                "Tipo do Veículo",
                value=chave_edit["tp_carro"],
                key="edit_tipo"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Salvar Alterações",
                    use_container_width=True
                ):

                    try:

                        atualizar_chave(
                            chave_edit["id"],
                            nova_chave,
                            novo_tipo
                        )

                        st.success(
                            "Chave atualizada com sucesso!"
                        )

                        st.session_state["editar_chave_id"] = None

                        st.rerun()

                    except Exception as erro:
                        st.error(str(erro))

            with col2:

                if st.button(
                    "❌ Cancelar",
                    use_container_width=True
                ):

                    st.session_state["editar_chave_id"] = None

                    st.rerun()

            st.divider()

    # ==========================
    # LISTAGEM
    # ==========================

    st.subheader("Chaves Cadastradas")

    busca_chave = st.text_input(
        "🔍 Buscar chave ou veículo",
        key="busca_chave_cadastro"
    )

    lista_chaves = listar_chaves()

    if busca_chave.strip():
        busca = busca_chave.strip().lower()

        lista_chaves = [
            item for item in lista_chaves
            if busca in str(item["chave"]).lower()
            or busca in str(item["tp_carro"]).lower()
        ]

    cab1, cab2, cab3, cab4 = st.columns(
        [2, 3, 1, 1]
    )

    with cab1:
        st.markdown("**Chave**")

    with cab2:
        st.markdown("**Veículo**")

    with cab3:
        st.markdown("**Editar**")

    with cab4:
        st.markdown("**Excluir**")

    st.divider()

    for item in lista_chaves:

        col1, col2, col3, col4 = st.columns(
            [2, 3, 1, 1]
        )

        with col1:
            st.write(item["chave"])

        with col2:
            st.write(item["tp_carro"])

        with col3:

            if st.button(
                "✏️",
                key=f"editar_{item['id']}"
            ):

                st.session_state["editar_chave_id"] = item["id"]

                st.rerun()

        with col4:

            if st.button(
                "🗑️",
                key=f"excluir_{item['id']}"
            ):

                try:

                    excluir_chave(item["id"])

                    st.success(
                        "Chave excluída com sucesso!"
                    )

                    st.rerun()

                except Exception as erro:

                    st.error(str(erro))

# ==================================
# MOTORISTAS
# ==================================

with aba2:

    st.subheader("Cadastrar Motorista")

    matricula = st.text_input(
        "Matrícula",
        key="nova_matricula"
    )

    nome = st.text_input(
        "Nome",
        key="novo_motorista"
    )

    if st.button(
        "Salvar Motorista",
        use_container_width=True
    ):
        
        if not matricula.strip() or not nome.strip():
            st.warning("Preencha todos os campos do motorista.")
            st.stop()

        try:

            cadastrar_motorista(
                matricula,
                nome
            )

            st.success(
                "Motorista cadastrado!"
            )

            st.rerun()

        except Exception as erro:

            st.error(str(erro))

    st.divider()

    # ==================================
    # EDIÇÃO
    # ==================================

    if st.session_state["editar_motorista_id"]:

        motorista = buscar_motorista_por_id(
            st.session_state["editar_motorista_id"]
        )

        if motorista:

            st.warning("Modo edição")

            nova_matricula = st.text_input(
                "Matrícula",
                value=motorista["matricula"],
                key="edit_matricula"
            )

            novo_nome = st.text_input(
                "Nome",
                value=motorista["nome"],
                key="edit_nome_motorista"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Salvar Alterações",
                    key="salvar_motorista",
                    use_container_width=True
                ):

                    try:

                        atualizar_motorista(
                            motorista["id"],
                            nova_matricula,
                            novo_nome
                        )

                        st.success(
                            "Motorista atualizado!"
                        )

                        st.session_state[
                            "editar_motorista_id"
                        ] = None

                        st.rerun()

                    except Exception as erro:

                        st.error(str(erro))

            with col2:

                if st.button(
                    "❌ Cancelar",
                    key="cancelar_motorista",
                    use_container_width=True
                ):

                    st.session_state[
                        "editar_motorista_id"
                    ] = None

                    st.rerun()

            st.divider()

    # ==================================
    # LISTAGEM
    # ==================================

    st.subheader("Motoristas Cadastrados")

    busca_motorista = st.text_input(
        "🔍 Buscar matrícula ou motorista",
        key="busca_motorista_cadastro"
    )

    lista_motoristas = listar_motoristas()

    if busca_motorista.strip():
        busca = busca_motorista.strip().lower()

        lista_motoristas = [
            item for item in lista_motoristas
            if busca in str(item["matricula"]).lower()
            or busca in str(item["nome"]).lower()
        ]

    cab1, cab2, cab3, cab4 = st.columns(
        [2, 4, 1, 1]
    )

    with cab1:
        st.markdown("**Matrícula**")

    with cab2:
        st.markdown("**Nome**")

    with cab3:
        st.markdown("**Editar**")

    with cab4:
        st.markdown("**Excluir**")

    st.divider()

    for item in lista_motoristas:

        col1, col2, col3, col4 = st.columns(
            [2, 4, 1, 1]
        )

        with col1:
            st.write(item["matricula"])

        with col2:
            st.write(item["nome"])

        with col3:

            if st.button(
                "✏️",
                key=f"editar_motorista_{item['id']}"
            ):

                st.session_state[
                    "editar_motorista_id"
                ] = item["id"]

                st.rerun()

        with col4:

            if st.button(
                "🗑️",
                key=f"excluir_motorista_{item['id']}"
            ):

                try:

                    excluir_motorista(
                        item["id"]
                    )

                    st.success(
                        "Motorista excluído!"
                    )

                    st.rerun()

                except Exception as erro:

                    st.error(str(erro))

# ==================================
# USUÁRIOS
# ==================================

with aba3:

    st.subheader(
        "Cadastrar Usuário"
    )

    username = st.text_input(
        "Usuário",
        key="novo_usuario"
    )

    senha = st.text_input(
        "Senha",
        type="password",
        key="nova_senha"
    )

    if st.session_state["nivel"] == "admin":

        niveis = [
            "admin",
            "usuario"
        ]

    else:

        niveis = [
            "usuario"
        ]

    nivel = st.selectbox(
        "Nível",
        niveis,
        key="novo_nivel"
    )

    if st.button(
        "Salvar Usuário",
        use_container_width=True
    ):
        
        if not username.strip() or not senha.strip():
            st.warning("Usuário e senha são obrigatórios.")
            st.stop()

        try:

            cadastrar_usuario(
                username,
                senha,
                nivel,
                st.session_state["nivel"]
            )

            st.success(
                "Usuário cadastrado!"
            )

            st.rerun()

        except Exception as erro:

            st.error(str(erro))

    st.divider()

    # ==================================
    # EDIÇÃO
    # ==================================

    if st.session_state["editar_usuario_id"]:

        usuario = buscar_usuario_por_id(
            st.session_state["editar_usuario_id"]
        )

        if usuario:

            st.warning("Modo edição")

            senha_edit = st.text_input(
                "Nova Senha",
                value=usuario["senha"],
                type="password",
                key="edit_senha_usuario"
            )

            nivel_edit = st.selectbox(
                "Nível",
                ["admin", "usuario"],
                index=0 if usuario["nivel"] == "admin" else 1,
                key="edit_nivel_usuario"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Salvar Alterações",
                    key="salvar_usuario",
                    use_container_width=True
                ):

                    try:

                        atualizar_usuario(
                            usuario["id"],
                            senha_edit,
                            nivel_edit
                        )

                        st.success(
                            "Usuário atualizado!"
                        )

                        st.session_state[
                            "editar_usuario_id"
                        ] = None

                        st.rerun()

                    except Exception as erro:

                        st.error(str(erro))

            with col2:

                if st.button(
                    "❌ Cancelar",
                    key="cancelar_usuario",
                    use_container_width=True
                ):

                    st.session_state[
                        "editar_usuario_id"
                    ] = None

                    st.rerun()

            st.divider()

    # ==================================
    # LISTAGEM
    # ==================================

    st.subheader(
        "Usuários Cadastrados"
    )

    cab1, cab2, cab3, cab4, cab5 = st.columns(
        [3, 2, 2, 1, 1]
    )

    with cab1:
        st.markdown("**Usuário**")

    with cab2:
        st.markdown("**Nível**")

    with cab3:
        st.markdown("**Status**")

    with cab4:
        st.markdown("**Editar**")

    with cab5:
        st.markdown("**Ação**")

    st.divider()

    for item in listar_usuarios():

        col1, col2, col3, col4, col5 = st.columns(
            [3, 2, 2, 1, 1]
        )

        with col1:
            st.write(item["username"])

        with col2:
            st.write(item["nivel"])

        with col3:
            st.write(item["status"])

        with col4:

            if st.button(
                "✏️",
                key=f"editar_usuario_{item['id']}"
            ):

                st.session_state[
                    "editar_usuario_id"
                ] = item["id"]

                st.rerun()

        with col5:

            if item["status"] == "Ativo":

                if st.button(
                    "Inativar",
                    key=f"inativar_{item['id']}"
                ):

                    try:

                        inativar_usuario(
                            item["id"]
                        )

                        st.success(
                            "Usuário inativado."
                        )

                        st.rerun()

                    except Exception as erro:

                        st.error(str(erro))

            else:

                if st.button(
                    "Ativar",
                    key=f"ativar_{item['id']}"
                ):

                    try:

                        ativar_usuario(
                            item["id"]
                        )

                        st.success(
                            "Usuário ativado."
                        )

                        st.rerun()

                    except Exception as erro:

                        st.error(str(erro))