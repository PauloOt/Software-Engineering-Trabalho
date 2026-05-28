"""
TaskFlow - Sistema de Gerenciamento de Tarefas
Empresa fictícia: TechFlow Solutions
Cliente: Startup de Logística
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Caminho do arquivo de dados (simula banco de dados simples)
DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


def proximo_id(tarefas):
    """Gera o próximo ID disponível."""
    if not tarefas:
        return 1
    return max(t["id"] for t in tarefas) + 1


# ─────────────────────────────────────────────
# ROTA RAIZ
# ─────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    """Rota de boas-vindas."""
    return jsonify({
        "sistema": "TaskFlow - Gerenciamento de Tarefas",
        "versao": "1.0.0",
        "rotas": {
            "GET  /tarefas":           "Lista todas as tarefas",
            "GET  /tarefas/<id>":      "Retorna uma tarefa específica",
            "POST /tarefas":           "Cria uma nova tarefa",
            "PUT  /tarefas/<id>":      "Atualiza uma tarefa existente",
            "DELETE /tarefas/<id>":    "Remove uma tarefa"
        }
    })


# ─────────────────────────────────────────────
# CREATE - Criar nova tarefa
# ─────────────────────────────────────────────

@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    """
    Cria uma nova tarefa.
    Body esperado (JSON):
      - titulo (obrigatório): string
      - descricao (opcional): string
      - prioridade (opcional): 'baixa' | 'media' | 'alta'
      - responsavel (opcional): string
    """
    dados = request.get_json()

    # Validação dos campos obrigatórios
    if not dados or not dados.get("titulo"):
        return jsonify({"erro": "O campo 'titulo' é obrigatório."}), 400

    titulo = dados["titulo"].strip()
    if not titulo:
        return jsonify({"erro": "O campo 'titulo' não pode ser vazio."}), 400

    prioridade = dados.get("prioridade", "media")
    if prioridade not in ("baixa", "media", "alta"):
        return jsonify({"erro": "Prioridade deve ser 'baixa', 'media' ou 'alta'."}), 400

    tarefas = carregar_tarefas()

    nova_tarefa = {
        "id":          proximo_id(tarefas),
        "titulo":      titulo,
        "descricao":   dados.get("descricao", ""),
        "status":      "a_fazer",          # a_fazer | em_progresso | concluido
        "prioridade":  prioridade,
        "responsavel": dados.get("responsavel", ""),
        "criado_em":   datetime.utcnow().isoformat(),
        "atualizado_em": datetime.utcnow().isoformat()
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)

    return jsonify(nova_tarefa), 201


# ─────────────────────────────────────────────
# READ - Listar todas as tarefas
# ─────────────────────────────────────────────

@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    """
    Lista todas as tarefas.
    Query params opcionais:
      - status: filtra por status
      - prioridade: filtra por prioridade
    """
    tarefas = carregar_tarefas()

    # Filtros opcionais via query string
    status_filtro = request.args.get("status")
    prioridade_filtro = request.args.get("prioridade")

    if status_filtro:
        tarefas = [t for t in tarefas if t["status"] == status_filtro]
    if prioridade_filtro:
        tarefas = [t for t in tarefas if t["prioridade"] == prioridade_filtro]

    return jsonify({"total": len(tarefas), "tarefas": tarefas})


# ─────────────────────────────────────────────
# READ - Buscar uma tarefa específica
# ─────────────────────────────────────────────

@app.route("/tarefas/<int:tarefa_id>", methods=["GET"])
def buscar_tarefa(tarefa_id):
    """Retorna uma tarefa pelo ID."""
    tarefas = carregar_tarefas()
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)

    if not tarefa:
        return jsonify({"erro": f"Tarefa com ID {tarefa_id} não encontrada."}), 404

    return jsonify(tarefa)


# ─────────────────────────────────────────────
# UPDATE - Atualizar tarefa existente
# ─────────────────────────────────────────────

@app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
def atualizar_tarefa(tarefa_id):
    """
    Atualiza uma tarefa existente.
    Campos atualizáveis: titulo, descricao, status, prioridade, responsavel
    """
    tarefas = carregar_tarefas()
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)

    if not tarefa:
        return jsonify({"erro": f"Tarefa com ID {tarefa_id} não encontrada."}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado para atualização."}), 400

    # Valida status se fornecido
    status_validos = ("a_fazer", "em_progresso", "concluido")
    if "status" in dados and dados["status"] not in status_validos:
        return jsonify({"erro": f"Status inválido. Use: {status_validos}"}), 400

    # Valida prioridade se fornecida
    prioridades_validas = ("baixa", "media", "alta")
    if "prioridade" in dados and dados["prioridade"] not in prioridades_validas:
        return jsonify({"erro": f"Prioridade inválida. Use: {prioridades_validas}"}), 400

    # Aplica as atualizações
    campos_editaveis = ("titulo", "descricao", "status", "prioridade", "responsavel")
    for campo in campos_editaveis:
        if campo in dados:
            tarefa[campo] = dados[campo]

    tarefa["atualizado_em"] = datetime.utcnow().isoformat()
    salvar_tarefas(tarefas)

    return jsonify(tarefa)


# ─────────────────────────────────────────────
# DELETE - Remover tarefa
# ─────────────────────────────────────────────

@app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
def deletar_tarefa(tarefa_id):
    """Remove uma tarefa pelo ID."""
    tarefas = carregar_tarefas()
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)

    if not tarefa:
        return jsonify({"erro": f"Tarefa com ID {tarefa_id} não encontrada."}), 404

    tarefas = [t for t in tarefas if t["id"] != tarefa_id]
    salvar_tarefas(tarefas)

    return jsonify({"mensagem": f"Tarefa '{tarefa['titulo']}' removida com sucesso."})


# ─────────────────────────────────────────────
# NOVO ESCOPO: Endpoint de estatísticas do projeto
# (mudança de escopo adicionada na Sprint 2)
# ─────────────────────────────────────────────

@app.route("/estatisticas", methods=["GET"])
def estatisticas():
    """
    Retorna estatísticas gerais do projeto.
    Feature adicionada na mudança de escopo (Sprint 2).
    """
    tarefas = carregar_tarefas()

    total = len(tarefas)
    a_fazer = sum(1 for t in tarefas if t["status"] == "a_fazer")
    em_progresso = sum(1 for t in tarefas if t["status"] == "em_progresso")
    concluido = sum(1 for t in tarefas if t["status"] == "concluido")

    por_prioridade = {
        "alta":  sum(1 for t in tarefas if t["prioridade"] == "alta"),
        "media": sum(1 for t in tarefas if t["prioridade"] == "media"),
        "baixa": sum(1 for t in tarefas if t["prioridade"] == "baixa"),
    }

    return jsonify({
        "total_tarefas": total,
        "por_status": {
            "a_fazer":      a_fazer,
            "em_progresso": em_progresso,
            "concluido":    concluido
        },
        "por_prioridade": por_prioridade,
        "percentual_conclusao": round((concluido / total * 100), 1) if total > 0 else 0
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
