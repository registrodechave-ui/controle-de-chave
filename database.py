from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================
# LOGIN
# ==========================

def autenticar_usuario(username, senha):
    resultado = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("username", username)
        .eq("senha", senha)
        .eq("status", "Ativo")
        .execute()
    )

    if resultado.data:
        return resultado.data[0]

    return None

# ==========================
# USUÁRIOS
# ==========================

def buscar_usuario(username, senha):
    resultado = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("username", username)
        .eq("senha", senha)
        .execute()
    )

    return resultado.data


# ==========================
# CHAVES
# ==========================

def listar_chaves():
    resultado = (
        supabase
        .table("chaves")
        .select("*")
        .order("chave")
        .execute()
    )

    return resultado.data


# ==========================
# MOTORISTAS
# ==========================

def listar_motoristas():
    resultado = (
        supabase
        .table("motoristas")
        .select("*")
        .order("nome")
        .execute()
    )

    return resultado.data

# ==========================
# BUSCAR MOTORISTAS
# ==========================

def buscar_motorista_por_id(id_motorista):

    resultado = (
        supabase
        .table("motoristas")
        .select("*")
        .eq("id", id_motorista)
        .execute()
    )

    if resultado.data:
        return resultado.data[0]

    return None

# ==========================
# LISTAR REGISTROS
# ==========================

def listar_registros():
    resultado = (
        supabase
        .table("registros")
        .select("*")
        .order("id", desc=True)
        .execute()
    )

    return resultado.data

# ==========================
# CADASTRAR CHAVE
# ==========================

def cadastrar_chave(chave, tp_carro):

    chave = chave.strip()
    tp_carro = tp_carro.strip()

    existente = (
        supabase
        .table("chaves")
        .select("*")
        .eq("chave", chave)
        .execute()
    )

    if existente.data:
        raise Exception("Esta chave já está cadastrada.")

    resultado = (
        supabase
        .table("chaves")
        .insert({
            "chave": chave,
            "tp_carro": tp_carro
        })
        .execute()
    )

    return resultado.data

# ==========================
# CADASTRAR MOTORISTA
# ==========================

def cadastrar_motorista(matricula, nome):

    matricula = matricula.strip()
    nome = nome.strip()

    existente = (
        supabase
        .table("motoristas")
        .select("*")
        .eq("matricula", matricula)
        .execute()
    )

    if existente.data:
        raise Exception("Esta matrícula já está cadastrada.")

    resultado = (
        supabase
        .table("motoristas")
        .insert({
            "matricula": matricula,
            "nome": nome
        })
        .execute()
    )

    return resultado.data

# ==========================
# BUSCAR MOTORISTA
# ==========================

def buscar_motorista(matricula):
    resultado = (
        supabase
        .table("motoristas")
        .select("*")
        .eq("matricula", matricula)
        .execute()
    )

    return resultado.data

# ==========================
# REGISTRAR SAÍDA
# ==========================

def registrar_saida(
    chave,
    tp_carro,
    matricula,
    nome,
    usuario_logado,
    status="Aberto",
    tipo_saida="Normal"
):
    aberto = (
        supabase
        .table("registros")
        .select("*")
        .eq("chave", chave)
        .in_("status", ["Aberto", "STV"])
        .execute()
    )

    if aberto.data:
        raise Exception(
            f"A chave {chave} já está em uso."
        )

    resultado = (
        supabase
        .table("registros")
        .insert({
            "chave": chave,
            "tp_carro": tp_carro,
            "matricula": matricula,
            "nome": nome,
            "data_saida": datetime.now().isoformat(),
            "status": status,
            "tipo_saida": tipo_saida,
            "usuario_saida": usuario_logado
        })
        .execute()
    )

    return resultado.data

# ==========================
# REGISTRAR DEVOLUÇÃO
# ==========================

def registrar_devolucao(
    chave,
    matricula_dev,
    nome_dev,
    usuario_logado
):
    aberto = (
        supabase
        .table("registros")
        .select("*")
        .eq("chave", chave)
        .in_("status", ["Aberto", "STV"])
        .execute()
    )

    if not aberto.data:
        raise Exception(
            f"A chave {chave} não possui saída em aberto ou STV."
        )

    registro = aberto.data[0]

    resultado = (
        supabase
        .table("registros")
        .update({
            "matricula_dev": matricula_dev,
            "nome_dev": nome_dev,
            "data_devolucao": datetime.now().isoformat(),
            "status": "Fechado",
            "usuario_devolucao": usuario_logado
        })
        .eq("id", registro["id"])
        .execute()
    )

    return resultado.data

# ==========================
# LISTAR CHAVES EM ABERTO
# ==========================

def listar_chaves_abertas():
    resultado = (
        supabase
        .table("registros")
        .select("*")
        .in_("status", ["Aberto", "STV"])
        .order("data_saida")
        .execute()
    )

    return resultado.data

# ==========================
# LISTAR CHAVES PARA DEVOLUÇÃO
# ==========================

def listar_chaves_para_devolucao():
    resultado = (
        supabase
        .table("registros")
        .select("*")
        .in_("status", ["Aberto", "STV"])
        .order("data_saida")
        .execute()
    )

    return resultado.data

# ==========================
# BUSCAR CHAVE
# ==========================

def buscar_chave(chave):
    resultado = (
        supabase
        .table("chaves")
        .select("*")
        .eq("chave", chave)
        .execute()
    )

    return resultado.data

# ==========================
# LISTAR CHAVE DISPONIVEL
# ==========================

def listar_chaves_disponiveis():
    todas = listar_chaves()

    abertas = listar_chaves_abertas()

    chaves_abertas = {
        item["chave"]
        for item in abertas
    }

    return [
        item
        for item in todas
        if item["chave"] not in chaves_abertas
    ]

# ==========================
# CADASTRAR USUÁRIO
# ==========================

def cadastrar_usuario(
    username,
    senha,
    nivel,
    usuario_logado_nivel
):

    if nivel == "admin":

        if usuario_logado_nivel != "admin":

            raise Exception(
                "Somente administradores podem criar usuários administradores."
            )

    existente = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if existente.data:

        raise Exception(
            "Usuário já cadastrado."
        )

    resultado = (
        supabase
        .table("usuarios")
        .insert({
            "username": username,
            "senha": senha,
            "nivel": nivel,
            "status": "Ativo"
        })
        .execute()
    )

    return resultado.data

# ==========================
# LISTAR USUÁRIOS
# ==========================

def listar_usuarios():
    resultado = (
        supabase
        .table("usuarios")
        .select("*")
        .order("username")
        .execute()
    )

    return resultado.data

# ==========================
# EXCLUIR CHAVE
# ==========================

def excluir_chave(id_chave):

    chave = (
        supabase
        .table("chaves")
        .select("*")
        .eq("id", id_chave)
        .execute()
    )

    if not chave.data:
        raise Exception("Chave não encontrada.")

    numero_chave = chave.data[0]["chave"]

    registros = (
        supabase
        .table("registros")
        .select("id")
        .eq("chave", numero_chave)
        .execute()
    )

    if registros.data:
        raise Exception(
            "Esta chave possui movimentações registradas e não pode ser excluída."
        )

    resultado = (
        supabase
        .table("chaves")
        .delete()
        .eq("id", id_chave)
        .execute()
    )

    return resultado.data

# ==========================
# ATUALIZAR CHAVE
# ==========================

def atualizar_chave(
    id_chave,
    chave,
    tp_carro
):

    chave = chave.strip()
    tp_carro = tp_carro.strip()

    existente =(
        supabase
        .table("chaves")
        .select("*")
        .eq("chave", chave)
        .neq("id", id_chave)
        .execute()
    )

    if existente.data:
        raise Exception("Esta chave já está cadastrada em outro registro")

    resultado = (
        supabase
        .table("chaves")
        .update({
            "chave": chave,
            "tp_carro": tp_carro
        })
        .eq("id", id_chave)
        .execute()
    )

    return resultado.data

# ==========================
# BUSCAR CHAVE POR ID
# ==========================

def buscar_chave_por_id(id_chave):

    resultado = (
        supabase
        .table("chaves")
        .select("*")
        .eq("id", id_chave)
        .execute()
    )

    if resultado.data:
        return resultado.data[0]

    return None

# ==========================
# ATUALIZAR MOTORISTAS
# ==========================

def atualizar_motorista(
    id_motorista,
    matricula,
    nome
):
    
    matricula = matricula.strip()
    nome = nome.strip()
    
    existente = (
        supabase
        .table("motoristas")
        .select("*")
        .eq("matricula", matricula)
        .neq("id", id_motorista)
        .execute()
    )

    if existente.data:
        raise Exception("Esta matrícula já está cadastrada em outro registro.")

    resultado = (
        supabase
        .table("motoristas")
        .update({
            "matricula": matricula,
            "nome": nome
        })
        .eq("id", id_motorista)
        .execute()
    )

    return resultado.data

# ==========================
# EXCLUIR MOTORISTAS
# ==========================

def excluir_motorista(id_motorista):

    motorista = (
        supabase
        .table("motoristas")
        .select("*")
        .eq("id", id_motorista)
        .execute()
    )

    if not motorista.data:
        raise Exception(
            "Motorista não encontrado."
        )

    matricula = motorista.data[0]["matricula"]

    registros_saida = (
        supabase
        .table("registros")
        .select("id")
        .eq("matricula", matricula)
        .execute()
    )

    registros_devolucao = (
        supabase
        .table("registros")
        .select("id")
        .eq("matricula_dev", matricula)
        .execute()
    )

    if registros_saida.data or registros_devolucao.data:

        raise Exception(
            "Este motorista possui movimentações registradas e não pode ser excluído."
        )

    resultado = (
        supabase
        .table("motoristas")
        .delete()
        .eq("id", id_motorista)
        .execute()
    )

    return resultado.data

# ==========================
# BUSCAR USUARIO POR ID
# ==========================

def buscar_usuario_por_id(id_usuario):

    resultado = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("id", id_usuario)
        .execute()
    )

    if resultado.data:
        return resultado.data[0]

    return None

# ==========================
# ATUALIZAR USUARIO
# ==========================

def atualizar_usuario(
    id_usuario,
    senha,
    nivel
):

    usuario = buscar_usuario_por_id(
        id_usuario
    )

    if not usuario:

        raise Exception(
            "Usuário não encontrado."
        )

    resultado = (
        supabase
        .table("usuarios")
        .update({
            "senha": senha,
            "nivel": nivel
        })
        .eq("id", id_usuario)
        .execute()
    )

    return resultado.data

# ==========================
# INATIVAR USUARIO
# ==========================

def inativar_usuario(id_usuario):

    usuario = buscar_usuario_por_id(
        id_usuario
    )

    if not usuario:

        raise Exception(
            "Usuário não encontrado."
        )

    if usuario["nivel"] == "admin":

        admins = (
            supabase
            .table("usuarios")
            .select("*")
            .eq("nivel", "admin")
            .eq("status", "Ativo")
            .execute()
        )

        if len(admins.data) <= 1:

            raise Exception(
                "Não é permitido inativar o último administrador do sistema."
            )

    resultado = (
        supabase
        .table("usuarios")
        .update({
            "status": "Inativo"
        })
        .eq("id", id_usuario)
        .execute()
    )

    return resultado.data

# ==========================
# ATIVAR USUARIO
# ==========================

def ativar_usuario(id_usuario):

    resultado = (
        supabase
        .table("usuarios")
        .update({
            "status": "Ativo"
        })
        .eq("id", id_usuario)
        .execute()
    )

    return resultado.data