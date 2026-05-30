#  Popula o TaskFlow com tarefas de exemplo para o pitch
#  Uso: .\popular_dados.ps1
#  (a API precisa estar rodando em http://localhost:5000)

$base = "http://localhost:5000"

Write-Host "`n>> Criando tarefas de exemplo no TaskFlow..." -ForegroundColor Cyan

$tarefas = @(
    @{ titulo = "Integrar API de rastreamento GPS";   prioridade = "alta";  responsavel = "Paulo" },
    @{ titulo = "Cadastrar frota de motoristas";       prioridade = "media"; responsavel = "Equipe Ops" },
    @{ titulo = "Desenhar tela de acompanhamento";     prioridade = "media"; responsavel = "Design" },
    @{ titulo = "Configurar pipeline de CI";           prioridade = "alta";  responsavel = "DevOps" },
    @{ titulo = "Documentar endpoints da API";         prioridade = "baixa"; responsavel = "Paulo" }
)

$ids = @()
foreach ($t in $tarefas) {
    $resp = Invoke-RestMethod -Uri "$base/tarefas" -Method Post -ContentType "application/json" -Body ($t | ConvertTo-Json)
    $ids += $resp.id
    Write-Host ("   [+] #{0}  {1}" -f $resp.id, $resp.titulo) -ForegroundColor Green
}

Write-Host "`n>> Movendo tarefas pelo Kanban..." -ForegroundColor Cyan

# Marca 1 como concluida e 2 como em progresso
Invoke-RestMethod -Uri "$base/tarefas/$($ids[3])" -Method Put -ContentType "application/json" -Body '{"status":"concluido"}'   | Out-Null
Write-Host "   [OK] #$($ids[3]) -> concluido" -ForegroundColor Green

Invoke-RestMethod -Uri "$base/tarefas/$($ids[0])" -Method Put -ContentType "application/json" -Body '{"status":"em_progresso"}' | Out-Null
Write-Host "   [OK] #$($ids[0]) -> em_progresso" -ForegroundColor Green

Invoke-RestMethod -Uri "$base/tarefas/$($ids[1])" -Method Put -ContentType "application/json" -Body '{"status":"em_progresso"}' | Out-Null
Write-Host "   [OK] #$($ids[1]) -> em_progresso" -ForegroundColor Green

Write-Host "`n>> Dados populados! Agora pode rodar o pitch." -ForegroundColor Yellow
Write-Host "   Sugestao: Invoke-RestMethod http://localhost:5000/estatisticas`n" -ForegroundColor Yellow
