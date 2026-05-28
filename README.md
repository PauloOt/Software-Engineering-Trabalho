# 📋 TaskFlow — Sistema de Gerenciamento de Tarefas

> Projeto desenvolvido para a disciplina de Engenharia de Software — UniFECAF  
> Empresa fictícia: **TechFlow Solutions** | Cliente: **Startup de Logística**

![CI Status](https://github.com/PauloOt/Software-Engineering-Trabalho/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.3-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Objetivo do Projeto

O **TaskFlow** é uma API REST de gerenciamento de tarefas desenvolvida para uma startup de logística. O sistema permite acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas e monitorar o desempenho da equipe — tudo alinhado às práticas de desenvolvimento ágil com **Kanban**.

---

## 📐 Escopo Inicial

As funcionalidades planejadas na Sprint 1 foram:

- CRUD completo de tarefas (Create, Read, Update, Delete)
- Filtro de tarefas por status e prioridade
- Estrutura de dados com campos: `titulo`, `descricao`, `status`, `prioridade`, `responsavel`
- Pipeline de CI com GitHub Actions (testes + lint)

---

## 🔄 Mudança de Escopo — Sprint 2

**Justificativa:** Durante a Sprint Review com o cliente (startup de logística), foi identificada a necessidade de um **dashboard de estatísticas** para que gestores possam visualizar rapidamente o progresso do projeto sem precisar consultar cada tarefa individualmente.

**Feature adicionada:**
- Endpoint `GET /estatisticas` que retorna:
  - Total de tarefas
  - Distribuição por status (A Fazer / Em Progresso / Concluído)
  - Distribuição por prioridade (Alta / Média / Baixa)
  - Percentual de conclusão do projeto

**Impacto no Kanban:** Novos cards foram criados nas colunas correspondentes para rastrear a implementação desta feature.

---

## 🛠️ Metodologia

Este projeto utiliza **Kanban** como metodologia ágil, com o quadro de tarefas organizado em:

| Coluna | Descrição |
|--------|-----------|
| 📌 A Fazer | Tarefas planejadas e ainda não iniciadas |
| 🔄 Em Progresso | Tarefas em desenvolvimento ativo |
| ✅ Concluído | Tarefas finalizadas e validadas |

---

## 🗂️ Estrutura do Repositório

```
taskflow/
├── src/
│   ├── app.py          # Aplicação Flask (CRUD + Estatísticas)
│   └── tasks.json      # Banco de dados local (gerado automaticamente)
├── tests/
│   └── test_app.py     # Testes automatizados com Pytest
├── docs/
│   └── parte_teorica.docx  # Documento teórico do trabalho
├── .github/
│   └── workflows/
│       └── ci.yml      # Pipeline de CI com GitHub Actions
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/PauloOt/Software-Engineering-Trabalho.git
cd Software-Engineering-Trabalho

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python src/app.py
```

A API estará disponível em: `http://localhost:5000`

---

## 📡 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Informações da API |
| `GET` | `/tarefas` | Lista todas as tarefas |
| `GET` | `/tarefas?status=a_fazer` | Filtra por status |
| `GET` | `/tarefas/<id>` | Retorna uma tarefa |
| `POST` | `/tarefas` | Cria nova tarefa |
| `PUT` | `/tarefas/<id>` | Atualiza tarefa |
| `DELETE` | `/tarefas/<id>` | Remove tarefa |
| `GET` | `/estatisticas` | Dashboard de estatísticas *(Sprint 2)* |

### Exemplo de criação de tarefa

```bash
curl -X POST http://localhost:5000/tarefas \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Implementar rastreamento de entregas",
    "descricao": "Integrar API de geolocalização",
    "prioridade": "alta",
    "responsavel": "Paulo"
  }'
```

---

## 🧪 Testes Automatizados

```bash
# Rodar todos os testes
pytest tests/ -v

# Com cobertura de código
pytest tests/ -v --cov=src --cov-report=term-missing
```

Os testes cobrem todos os endpoints CRUD, validações de entrada e o endpoint de estatísticas.

---

## ⚙️ Pipeline CI/CD

O arquivo `.github/workflows/ci.yml` executa automaticamente a cada push ou pull request:

1. **Testes automatizados** com Pytest + cobertura de código
2. **Análise de qualidade** com Flake8 (lint)

---

## 👥 Equipe

| Nome | RA | Papel |
|------|----|-------|
| Paulo | 166037 | Desenvolvedor / Gestor / DevOps |

---

## 📚 Referências

- [Documentação Flask](https://flask.palletsprojects.com/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pytest Docs](https://docs.pytest.org/)
- Pressman, R. — *Engenharia de Software: Uma Abordagem Profissional*
