import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
from auth import verificar_admin

verificar_admin()

from database import (
    listar_registros
)

def gerar_excel(df):

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Relatorio"
        )

    buffer.seek(0)

    return buffer

st.title("📊 Relatórios")

dados = listar_registros()

if not dados:

    st.warning(
        "Nenhum registro encontrado."
    )

    st.stop()

df = pd.DataFrame(dados)

# ==================================
# CONVERTE DATAS
# ==================================

if "data_saida" in df.columns:

    df["data_saida"] = pd.to_datetime(
        df["data_saida"],
        errors="coerce"
    )

if "data_devolucao" in df.columns:

    df["data_devolucao"] = pd.to_datetime(
        df["data_devolucao"],
        errors="coerce"
    )

# ==================================
# FILTROS
# ==================================

st.subheader("🔍 Filtros")

col1, col2, col3 = st.columns(3)

with col1:

    chave_filtro = st.text_input(
        "🔑 Chave",
    )

with col2:

    motorista_filtro = st.text_input(
        "👤 Motorista",
    )

with col3:

    lista_tipos = sorted(
        df["tipo_saida"]
        .dropna()
        .unique()
        .tolist()
    )

    tipo_saida_filtro = st.selectbox(
        "🚗 Tipo Saída",
        ["Todos"] + lista_tipos
    )

col3, col4, col5 = st.columns(3)

with col3:

    status_filtro = st.selectbox(
        "📌 Status",
        [
            "Todos",
            "Aberto",
            "Fechado",
            "STV"
        ]
    )

with col4:

    data_inicial = st.date_input(
        "📅 Data Inicial",
        value=datetime.now().date() - timedelta(days=30),
        format="DD/MM/YYYY"
    )

with col5:

    data_final = st.date_input(
        "📅 Data Final",
        value=datetime.now().date(),
        format="DD/MM/YYYY"
    )

# ==================================
# APLICA FILTROS
# ==================================

df_filtrado = df.copy()

if chave_filtro.strip():

    df_filtrado = df_filtrado[
        df_filtrado["chave"]
        .astype(str)
        .str.contains(
            chave_filtro.strip(),
            case=False,
            na=False
        )
    ]

if motorista_filtro.strip:

    df_filtrado = df_filtrado[
        df_filtrado["nome"]
        .astype(str)
        .str.contains(
            motorista_filtro.strip(),
            case=False,
            na=False
        )
    ]

if tipo_saida_filtro != "Todos":

    df_filtrado = df_filtrado[
        df_filtrado["tipo_saida"] == tipo_saida_filtro
    ]

if status_filtro != "Todos":

    df_filtrado = df_filtrado[
        df_filtrado["status"] == status_filtro
    ]

if "data_saida" in df_filtrado.columns:

    df_filtrado = df_filtrado[
        (
            df_filtrado["data_saida"]
            .dt.date >= data_inicial
        )
        &
        (
            df_filtrado["data_saida"]
            .dt.date <= data_final
        )
    ]

# ==================================
# INDICADORES
# ==================================

total_mov = len(df_filtrado)

em_uso = len(
    df_filtrado[
        df_filtrado["status"] == "Aberto"
    ]
)

stv = len(
    df_filtrado[
        df_filtrado["status"] == "STV"
    ]
)

fechados = len(
    df_filtrado[
        df_filtrado["status"] == "Fechado"
    ]
)

motoristas = (
    df_filtrado["matricula"]
    .nunique()
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "🔑 Movimentações",
        total_mov
    )

with col2:

    st.metric(
        "🔓 Em Uso",
        em_uso
    )

with col3:

    st.metric(
        "🟡 STV",
        stv
    )

with col4:

    st.metric(
        "✅ Fechadas",
        fechados
    )

with col5:

    st.metric(
        "👤 Motoristas",
        motoristas
    )

st.divider()

# ==================================
# TABELA
# ==================================

colunas = [
    "chave",
    "tp_carro",
    "matricula",
    "nome",
    "matricula_dev",
    "nome_dev",
    "usuario_saida",
    "usuario_devolucao",
    "data_saida",
    "data_devolucao",
    "status",
    "tipo_saida"
]

existentes = [
    coluna
    for coluna in colunas
    if coluna in df_filtrado.columns
]

df_exibicao = df_filtrado[existentes].copy()

if "data_saida" in df_exibicao.columns:
    df_exibicao["data_saida"] = (
        df_exibicao["data_saida"]
        .dt.strftime("%d/%m/%Y %H:%M:%S")
    )

if "data_devolucao" in df_exibicao.columns:
    df_exibicao["data_devolucao"] = (
        df_exibicao["data_devolucao"]
        .dt.strftime("%d/%m/%Y %H:%M:%S")
    )

df_exibicao = df_exibicao.rename(columns={
    "chave": "Chave",
    "tp_carro": "Veículo",
    "matricula": "Matrícula",
    "nome": "Motorista Retirada",
    "matricula_dev": "Matrícula Devolução",
    "nome_dev": "Motorista Devolução",
    "usuario_saida": "Usuário Saída",
    "usuario_devolucao": "Usuário Devolução",
    "data_saida": "Data Saída",
    "data_devolucao": "Data Devolução",
    "status": "Status",
    "tipo saida": "tipo_saida"
})

st.dataframe(
    df_exibicao,
    use_container_width=True
)

# ==================================
# EXPORTAR EXCEL
# ==================================

st.divider()

df_excel = df_filtrado[existentes].copy()

if "data_saida" in df_excel.columns:
    df_excel["data_saida"] = (
        pd.to_datetime(
            df_excel["data_saida"],
            errors="coerce"
        )
        .dt.strftime("%d/%m/%Y %H:%M:%S")
    )

if "data_devolucao" in df_excel.columns:
    df_excel["data_devolucao"] = (
        pd.to_datetime(
            df_excel["data_devolucao"],
            errors="coerce"
        )
        .dt.strftime("%d/%m/%Y %H:%M:%S")
    )

excel = gerar_excel(
    df_excel
)

st.download_button(
    label="📥 Exportar Excel",
    data=excel,
    file_name=f"relatorio_chaves_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)