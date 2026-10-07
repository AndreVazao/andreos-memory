# 🚀 QUICK START - Ollama + Claude Token Optimization

## 📋 PRÉ-CHECKLIST

- [x] Ollama instalado e rodando (version 0.23.0)
- [x] 7 modelos instalados (986MB - 2GB cada)
- [x] Servidor ouvindo em http://127.0.0.1:11434
- [x] Scripts Python criados em C:\AI\
- [x] Documentação em Obsidian

---

## 🎯 TAREFAS RÁPIDAS (Copiar e colar)

### 1. Testar Ollama direto (PowerShell - 2 min)

```powershell
# Verificar que está rodando
ollama list

# Teste rápido (llama3.2:1b)
$body = @{
    model = "llama3.2:1b"
    prompt = "Resuma em uma linha: Inteligência artificial é o futuro da tecnologia"
    stream = $false
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/generate" `
    -Method Post -Body $body -ContentType "application/json" | `
    Select-Object -ExpandProperty Content | ConvertFrom-Json | `
    Select-Object -ExpandProperty response
```

**Resultado esperado**: Resposta em 2-5 minutos (CPU-only)

---

### 2. Instalar dependências Python (PowerShell - 3 min)

```powershell
cd C:\AI
python -m venv venv
venv\Scripts\activate
pip install requests anthropic --break-system-packages

# Verificar instalação
python -c "import requests, anthropic; print('✅ OK')"
```

---

### 3. Rodar MCP Server (PowerShell - 5 min)

```powershell
cd C:\AI
venv\Scripts\activate
python ollama_mcp_server.py

# Será mostrado menu interativo:
# 1. summarize
# 2. code_generation
# 3. analyze
# 4. classify
# 5. extract
#
# Escolher opção (ex: 1)
# Entrar com prompt
# Ver resposta + tokens + economia
```

---

### 4. Rodar Hybrid Agent (PowerShell - 5 min)

```powershell
cd C:\AI
venv\Scripts\activate
python claude_ollama_hybrid.py

# Opções:
# > analyze
# > sample
# > report
# > quit

# Exemplo de uso:
# > sample
# (mostra análise de 5 tarefas reais)
#
# > analyze
# Enter task: Summarize this long document about...
# (recomenda Ollama vs Claude com economia estimada)
```

---

### 5. Integrar com Claude API (Python - 10 min)

```python
# Arquivo: seu_script.py
from claude_ollama_production import ClaudeOllamaHybrid

# Inicializar
client = ClaudeOllamaHybrid()

# Tarefa simples
resultado = client.route_task(
    task_type="summarize",
    prompt="Resuma este documento em 2 frases..."
)

print(f"✅ Modelo: {resultado.model}")
print(f"💬 Resposta: {resultado.response}")
print(f"💰 Custo: ${resultado.cost:.6f}")
print(f"💎 Economia: ${resultado.savings:.6f}")
```

---

## 🔧 CONFIGURAÇÃO (Uma única vez)

### Auto-start Ollama no Windows (Opcional mas recomendado)

**Método 1: Via PowerShell (Admin)**
```powershell
# Abrir PowerShell como Admin, depois:

$action = New-ScheduledTaskAction `
    -Execute "C:\Users\André Vazão\AppData\Local\Programs\Ollama\ollama.exe" `
    -Argument "serve"

$trigger = New-ScheduledTaskTrigger -AtLogOn

Register-ScheduledTask `
    -TaskName "Ollama Auto-Start" `
    -Action $action `
    -Trigger $trigger `
    -RunLevel Highest

# Verificar:
Get-ScheduledTask -TaskName "Ollama Auto-Start"
```

**Método 2: Criar batch file**
```batch
# Arquivo: C:\Users\André Vazão\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ollama.bat

@echo off
:loop
"C:\Users\André Vazão\AppData\Local\Programs\Ollama\ollama.exe" serve
timeout /t 5
goto loop
```

---

## 📊 CHEAT SHEET - Qual modelo para cada tarefa?

| Tarefa | Modelo | Tempo | Qualidade | Economia |
|--------|--------|-------|-----------|----------|
| Resumir texto | llama3.2:1b | ⚡⚡⚡ | ⭐⭐⭐⭐⭐⭐ | 60% |
| Formatar dados | llama3.2:1b | ⚡⚡⚡ | ⭐⭐⭐⭐⭐⭐⭐ | 50% |
| Gerar código | qwen2.5-coder | ⚡⚡ | ⭐⭐⭐⭐⭐⭐⭐⭐ | 55% |
| Analisar | llama3.2:3b | ⚡ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐ | 40% |
| Raciocinar | deepseek-r1 | ⚡⚡ | ⭐⭐⭐⭐⭐⭐⭐⭐ | 45% |
| Context search | gemma2:2b | ⚡⚡ | ⭐⭐⭐⭐⭐⭐⭐ | 50% |

---

## 🎮 MODO INTERATIVO (Sem código)

Se quiser testar sem escrever código:

```powershell
# Abrir PowerShell, rodar:
python C:\AI\ollama_mcp_server.py

# Escolher número de tarefa
# Entrar com texto
# Ver resultado

# Exemplo:
# > Choose task:
# > 1. summarize
# > 2. code_generation
# > 3. analyze
# > 
# > Enter choice: 1
# > Enter prompt for summarize: O Ollama é um modelo de linguagem local...
# > 
# > 🔄 Using model: llama3.2:1b
# > Generating response...
# > 
# > ✅ Response:
# > O Ollama é uma ferramenta para executar modelos de IA localmente.
# > 
# > 📊 Tokens: 23
# > 💰 Estimated savings: $0.000069
# > Total savings this session: $0.000069
```

---

## 💡 DICAS DE USO

### Dica 1: Usar Ollama para "rascunho"
```
Fluxo:
1. Ollama gera rascunho rápido (gratuito)
2. Claude refina resultado final (pagos, mas menos tokens)
3. Resultado: Economiza 30-50% tokens, mesma qualidade
```

### Dica 2: Batch processing
```powershell
# Se tem 50 documentos para resumir:
# - Summarize 50 x com llama3.2:1b (grátis): ~$0
# - Refinar 5 melhores com Claude (pagos): ~$0.30
# vs
# - Resumir todos 50 com Claude: ~$1.50
# Economia: 80%!
```

### Dica 3: Cache de respostas
```python
# Se pergunta é frequente, cache resultado Ollama
respostas_cache = {
    "O que é Ollama?": "Ollama é...",
    "Modelos disponíveis?": "llama3.2:3b, llama3.2:1b...",
}

def responder(pergunta):
    if pergunta in respostas_cache:
        return respostas_cache[pergunta]  # Grátis!
    return ollama.generate(pergunta)  # Ou Claude se necessário
```

---

## ❌ EVITAR

### ❌ NÃO use Ollama para:
- Decisões críticas (use Claude)
- Conteúdo legal/compliance (use Claude)
- Criatividade alta (Claude é melhor)
- Tasks com <100 tokens (overhead não vale)
- Anything where quality < 7/10 é inaceitável

### ❌ NÃO confunda:
- `llama3.2:1b` (1 bilhão parâmetros, rápido)
- `llama3.2:3b` (3 bilhões parâmetros, melhor qualidade)
- Ambos no mesmo servidor, escolha certo!

---

## 📈 MONITORAMENTO

### Spreadsheet de tracking (CSV)

```csv
Data,Tarefa,Modelo,Tokens,Custo,Economia,Tempo
2026-06-06,Summarize,llama3.2:1b,150,0,0.00045,2min
2026-06-06,Code Review,qwen2.5-coder,200,0,0.0003,3min
2026-06-06,Analyze,claude-sonnet-4,500,0.0045,0,8sec
```

Usar para:
- Validar economia real vs. estimada
- Identificar tarefas que se beneficiam mais
- Ajustar threshold de qualidade

---

## 🆘 TROUBLESHOOTING

### P: Ollama diz "Connection refused"
**R**: Restarts Ollama
```powershell
taskkill /IM ollama.exe /F
ollama serve
```

### P: Python "No module named requests"
**R**: Instalar deps novamente
```powershell
pip install requests anthropic --break-system-packages
```

### P: Resposta muito lenta (5+ min)
**R**: Normal em CPU. Use `llama3.2:1b` ao invés de `3b`

### P: Qualidade do Ollama ruim
**R**: Aumentar temperatura/top_p, ou usar Claude para refinamento

---

## 📞 CONTATOS RÁPIDOS

- **Ollama API**: `http://127.0.0.1:11434`
- **Documentos**: `C:\AndreOS-Memory\04 - Development Memory\`
- **Scripts**: `C:\AI\`
- **Modelos**: `C:\Users\André Vazão\.ollama\models`

---

## ✅ CHECKLIST POR DIA

**Segunda (Hoje)**:
- [x] Ollama a rodar
- [ ] Testar PowerShell (10 min)
- [ ] Instalar Python deps (5 min)

**Terça**:
- [ ] Rodar ollama_mcp_server.py (15 min)
- [ ] Testar 3 tarefas diferentes
- [ ] Documentar tempo/qualidade

**Quarta**:
- [ ] Rodar claude_ollama_hybrid.py (10 min)
- [ ] Analisar 5 tarefas do seu workflow
- [ ] Medir economia real

**Quinta+**:
- [ ] Integrar em seu workflow
- [ ] Monitorar economia
- [ ] Ajustar regras

---

**Última atualização**: 2026-06-06 16:45 UTC  
**Versão**: 1.0  
**Status**: Pronto para usar! 🚀

Qualquer dúvida, run: `python C:\AI\ollama_mcp_server.py` e explore!
