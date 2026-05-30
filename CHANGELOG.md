# Changelog

Histórico de mudanças do projeto TaskFlow.
Segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [1.1.0] — Sprint 2

### Adicionado
- Endpoint `GET /estatisticas` com dashboard de progresso do projeto
  - Total de tarefas
  - Distribuição por status (a_fazer / em_progresso / concluido)
  - Distribuição por prioridade (alta / media / baixa)
  - Percentual de conclusão
- Testes automatizados para o endpoint de estatísticas
- Script `popular_dados.ps1` para popular dados de demonstração
- Arquivo `LICENSE` (MIT)

### Justificativa da mudança de escopo
Durante a Sprint Review com o cliente (startup de logística), foi identificada
a necessidade de um dashboard para gestores acompanharem o progresso sem
precisar consultar cada tarefa individualmente.

## [1.0.0] — Sprint 1

### Adicionado
- API REST em Flask com CRUD completo de tarefas
  - `POST /tarefas` — criar tarefa
  - `GET /tarefas` — listar (com filtros por status e prioridade)
  - `GET /tarefas/<id>` — buscar por id
  - `PUT /tarefas/<id>` — atualizar
  - `DELETE /tarefas/<id>` — remover
- Persistência local em arquivo JSON
- Validação de entrada para `titulo` e `prioridade`
- Pipeline de CI com GitHub Actions (Pytest + Flake8)
- Suite de testes automatizados com cobertura de código
