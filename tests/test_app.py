"""
Testes automatizados para o TaskFlow
Utiliza pytest + cliente de teste do Flask
"""

import pytest
import json
import os
import sys

# Garante que o módulo src seja encontrado
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from app import app, DATA_FILE


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def cliente():
    """Configura o cliente de teste com arquivo de dados temporário."""
    app.config["TESTING"] = True

    # Usa arquivo temporário para não afetar dados reais
    import tempfile
    tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp.write(b"[]")
    tmp.close()

    import app as app_module
    original = app_module.DATA_FILE
    app_module.DATA_FILE = tmp.name

    with app.test_client() as c:
        yield c

    app_module.DATA_FILE = original
    os.unlink(tmp.name)


# ─────────────────────────────────────────────
# TESTES DA ROTA RAIZ
# ─────────────────────────────────────────────

def test_rota_raiz(cliente):
    """Verifica se a rota raiz retorna 200 e informações do sistema."""
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    dados = json.loads(resposta.data)
    assert "sistema" in dados
    assert "rotas" in dados


# ─────────────────────────────────────────────
# TESTES: CREATE
# ─────────────────────────────────────────────

def test_criar_tarefa_valida(cliente):
    """Cria uma tarefa com todos os campos válidos."""
    payload = {
        "titulo": "Implementar autenticação",
        "descricao": "Criar sistema de login com JWT",
        "prioridade": "alta",
        "responsavel": "Pedro"
    }
    resposta = cliente.post("/tarefas", json=payload)
    assert resposta.status_code == 201
    dados = json.loads(resposta.data)
    assert dados["titulo"] == "Implementar autenticação"
    assert dados["status"] == "a_fazer"
    assert dados["prioridade"] == "alta"
    assert dados["id"] == 1


def test_criar_tarefa_sem_titulo(cliente):
    """Deve retornar erro 400 quando titulo não é enviado."""
    resposta = cliente.post("/tarefas", json={"descricao": "Sem título"})
    assert resposta.status_code == 400
    dados = json.loads(resposta.data)
    assert "erro" in dados


def test_criar_tarefa_titulo_vazio(cliente):
    """Deve retornar erro 400 quando titulo é string vazia."""
    resposta = cliente.post("/tarefas", json={"titulo": "   "})
    assert resposta.status_code == 400


def test_criar_tarefa_prioridade_invalida(cliente):
    """Deve retornar erro 400 para prioridade inválida."""
    resposta = cliente.post("/tarefas", json={"titulo": "Tarefa X", "prioridade": "urgente"})
    assert resposta.status_code == 400


def test_criar_tarefa_prioridade_padrao(cliente):
    """Tarefa sem prioridade deve usar 'media' como padrão."""
    resposta = cliente.post("/tarefas", json={"titulo": "Tarefa padrão"})
    assert resposta.status_code == 201
    dados = json.loads(resposta.data)
    assert dados["prioridade"] == "media"


# ─────────────────────────────────────────────
# TESTES: READ
# ─────────────────────────────────────────────

def test_listar_tarefas_vazia(cliente):
    """Lista vazia deve retornar total 0."""
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200
    dados = json.loads(resposta.data)
    assert dados["total"] == 0
    assert dados["tarefas"] == []


def test_listar_tarefas_com_dados(cliente):
    """Deve listar as tarefas criadas."""
    cliente.post("/tarefas", json={"titulo": "Tarefa 1"})
    cliente.post("/tarefas", json={"titulo": "Tarefa 2"})
    resposta = cliente.get("/tarefas")
    dados = json.loads(resposta.data)
    assert dados["total"] == 2


def test_buscar_tarefa_existente(cliente):
    """Deve retornar a tarefa correta pelo ID."""
    cliente.post("/tarefas", json={"titulo": "Tarefa Específica", "responsavel": "Paulo"})
    resposta = cliente.get("/tarefas/1")
    assert resposta.status_code == 200
    dados = json.loads(resposta.data)
    assert dados["titulo"] == "Tarefa Específica"
    assert dados["responsavel"] == "Paulo"


def test_buscar_tarefa_inexistente(cliente):
    """Deve retornar 404 para ID que não existe."""
    resposta = cliente.get("/tarefas/999")
    assert resposta.status_code == 404


def test_filtrar_por_status(cliente):
    """Deve filtrar tarefas por status."""
    cliente.post("/tarefas", json={"titulo": "Tarefa A"})
    cliente.post("/tarefas", json={"titulo": "Tarefa B"})
    cliente.put("/tarefas/1", json={"status": "concluido"})

    resposta = cliente.get("/tarefas?status=concluido")
    dados = json.loads(resposta.data)
    assert dados["total"] == 1
    assert dados["tarefas"][0]["titulo"] == "Tarefa A"


# ─────────────────────────────────────────────
# TESTES: UPDATE
# ─────────────────────────────────────────────

def test_atualizar_tarefa(cliente):
    """Deve atualizar campos de uma tarefa existente."""
    cliente.post("/tarefas", json={"titulo": "Original"})
    resposta = cliente.put("/tarefas/1", json={
        "titulo": "Atualizado",
        "status": "em_progresso",
        "prioridade": "alta"
    })
    assert resposta.status_code == 200
    dados = json.loads(resposta.data)
    assert dados["titulo"] == "Atualizado"
    assert dados["status"] == "em_progresso"
    assert dados["prioridade"] == "alta"


def test_atualizar_tarefa_status_invalido(cliente):
    """Deve retornar erro para status inválido."""
    cliente.post("/tarefas", json={"titulo": "Tarefa"})
    resposta = cliente.put("/tarefas/1", json={"status": "cancelado"})
    assert resposta.status_code == 400


def test_atualizar_tarefa_inexistente(cliente):
    """Deve retornar 404 ao tentar atualizar tarefa que não existe."""
    resposta = cliente.put("/tarefas/999", json={"titulo": "Não existe"})
    assert resposta.status_code == 404


# ─────────────────────────────────────────────
# TESTES: DELETE
# ─────────────────────────────────────────────

def test_deletar_tarefa(cliente):
    """Deve remover uma tarefa existente."""
    cliente.post("/tarefas", json={"titulo": "Para deletar"})
    resposta = cliente.delete("/tarefas/1")
    assert resposta.status_code == 200
    dados = json.loads(resposta.data)
    assert "mensagem" in dados

    # Confirma que foi removida
    resposta2 = cliente.get("/tarefas/1")
    assert resposta2.status_code == 404


def test_deletar_tarefa_inexistente(cliente):
    """Deve retornar 404 ao tentar deletar tarefa inexistente."""
    resposta = cliente.delete("/tarefas/999")
    assert resposta.status_code == 404


# ─────────────────────────────────────────────
# TESTES: ESTATÍSTICAS (mudança de escopo)
# ─────────────────────────────────────────────

def test_estatisticas_vazio(cliente):
    """Estatísticas com base vazia deve retornar zeros."""
    resposta = cliente.get("/estatisticas")
    assert resposta.status_code == 200
    dados = json.loads(resposta.data)
    assert dados["total_tarefas"] == 0
    assert dados["percentual_conclusao"] == 0


def test_estatisticas_com_dados(cliente):
    """Deve calcular percentual de conclusão corretamente."""
    cliente.post("/tarefas", json={"titulo": "T1", "prioridade": "alta"})
    cliente.post("/tarefas", json={"titulo": "T2", "prioridade": "baixa"})
    cliente.put("/tarefas/1", json={"status": "concluido"})

    resposta = cliente.get("/estatisticas")
    dados = json.loads(resposta.data)
    assert dados["total_tarefas"] == 2
    assert dados["por_status"]["concluido"] == 1
    assert dados["percentual_conclusao"] == 50.0
    assert dados["por_prioridade"]["alta"] == 1
