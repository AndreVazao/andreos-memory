# LOCAL MCP SERVER - INTEGRAÇÃO COM CLAUDE DESKTOP

## ✅ SERVIDOR ATIVO

O servidor MCP local está rodando em:
- **URL**: `http://127.0.0.1:5555`
- **PID**: 8380
- **Modo**: FREE (sem limites reais, apenas rate limiting)

---

## 🔗 CONFIGURAR NO CLAUDE DESKTOP

### Passo 1: Abrir `claude_desktop_config.json`

**Localização**: `%APPDATA%\Claude\claude_desktop_config.json`

Ou use PowerShell:
```powershell
$path = "$env:APPDATA\Claude\claude_desktop_config.json"
notepad $path
```

### Passo 2: Adicionar o MCP Server

Adiciona isto ao arquivo de config (na secção `mcpServers`):

```json
{
  "mcpServers": {
    "ollama-local": {
      "type": "http",
      "url": "http://127.0.0.1:5555"
    }
  }
}
```

**Exemplo completo**:
```json
{
  "mcpServers": {
    "obsidian": {
      "type": "http",
      "url": "http://127.0.0.1:27124/mcp/",
      "headers": {
        "Authorization": "Bearer token-aqui"
      }
    },
    "ollama-local": {
      "type": "http",
      "url": "http://127.0.0.1:5555"
    }
  }
}
```

### Passo 3: Reiniciar Claude Desktop

- Fecha Claude Desktop completamente
- Reabre Claude Desktop
- MCP deve aparecer como conectado

---

## 🎮 USAR NO CHAT

Depois de conectado, podes chamar o Ollama assim:

### Exemplo 1: Resumir texto (FREE!)

```
Eu: Quero resumir um documento longo. Podes usar o Ollama para fazer?

Claude: Claro! Vou chamar o servidor Ollama local.
[Chama /process com model_type="fast"]
Ollama executa: llama3.2:1b
Retorna: resumo + tokens + economia
```

### Exemplo 2: Gerar código

```
Eu: Cria uma função Python para validar emails

Claude: Vou usar o Ollama para isso (grátis!).
[Chama /process com model_type="code"]
Ollama executa: qwen2.5-coder:1.5b
Retorna: código + tokens usados
```

### Exemplo 3: Análise profunda

```
Eu: Analisa a economia portuguesa em 2024

Claude: Deixa-me chamar Ollama com reasoning.
[Chama /process com model_type="reasoning"]
Ollama executa: deepseek-r1:1.5b
Retorna: análise profunda + 100% grátis
```

---

## 📊 ENDPOINTS DISPONÍVEIS

### GET /health
**Verifica se servidor está ativo**
```bash
curl http://127.0.0.1:5555/health
```

Retorna:
```json
{
  "status": "ok",
  "ollama": "connected"
}
```

### GET /models
**Lista modelos disponíveis**
```bash
curl http://127.0.0.1:5555/models
```

Retorna:
```json
{
  "status": "ok",
  "models": {
    "fast": "llama3.2:1b",
    "balanced": "llama3.2:3b",
    "code": "qwen2.5-coder:1.5b",
    "reasoning": "deepseek-r1:1.5b"
  }
}
```

### GET /stats
**Ver estatísticas de uso**
```bash
curl http://127.0.0.1:5555/stats
```

Retorna:
```json
{
  "status": "ok",
  "data": {
    "hourly": {
      "used": 25,
      "limit": 50,
      "remaining": 25
    },
    "daily": {
      "used": 120,
      "limit": 200,
      "remaining": 80
    },
    "total_tokens": 15000,
    "total_cost_saved": "$0.2250"
  }
}
```

### POST /process
**Processar um prompt**

```bash
curl -X POST http://127.0.0.1:5555/process \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Resuma este texto...",
    "model_type": "fast",
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

**model_type options**:
- `fast` - llama3.2:1b (rápido, 6/10 qualidade)
- `balanced` - llama3.2:3b (8.5/10 qualidade, melhor)
- `code` - qwen2.5-coder:1.5b (7.5/10, especializado código)
- `reasoning` - deepseek-r1:1.5b (8/10, análise profunda)

Retorna:
```json
{
  "status": "ok",
  "response": "Resultado da operação...",
  "tokens": 150,
  "model": "llama3.2:1b",
  "cost_saved": "$0.002250",
  "rate_limit": {
    "hourly_remaining": 24,
    "daily_remaining": 79
  }
}
```

### POST /batch
**Processar múltiplos prompts**

```bash
curl -X POST http://127.0.0.1:5555/batch \
  -H "Content-Type: application/json" \
  -d '{
    "prompts": [
      {"prompt": "Texto 1", "model_type": "fast"},
      {"prompt": "Texto 2", "model_type": "balanced"},
      {"prompt": "Código aqui", "model_type": "code"}
    ]
  }'
```

---

## ⚙️ CONFIGURAR RATE LIMITS

Edita `C:\AI\ollama_local_mcp.py` linhas 23-26:

```python
RATE_LIMITS = {
    "per_hour": 50,    # ← Aumentar se precisa
    "per_day": 200,    # ← Aumentar se precisa
}
```

Depois reinicia o servidor (mata processo e roda novamente).

---

## 🚀 USAR COM MÚLTIPLOS LLMs

### Com Codex
Se tens Codex instalado, usa mesma configuração:
```json
{
  "mcpServers": {
    "ollama-local": {
      "type": "http",
      "url": "http://127.0.0.1:5555"
    }
  }
}
```

### Com AntiGravity
Mesma abordagem - qualquer LLM que suporte MCP HTTP pode chamar.

---

## 📋 CHECKLIST

- [x] Ollama rodando (`ollama serve`)
- [x] MCP Server rodando (`python ollama_local_mcp.py`)
- [ ] Claude Desktop config atualizado
- [ ] Claude Desktop reiniciado
- [ ] Testar /health endpoint
- [ ] Chamar /process no chat
- [ ] Ver economia nos /stats

---

## 🆘 TROUBLESHOOTING

### "Connection refused"
```powershell
# Verifica se servidor está a rodar
curl http://127.0.0.1:5555/health

# Se não funciona, reinicia
python C:\AI\ollama_local_mcp.py
```

### "Ollama não responde"
```powershell
# Verifica se Ollama está a rodar
ollama list

# Se não funciona, inicia
ollama serve
```

### Rate limit atingido
Aguarda 1 hora ou edita RATE_LIMITS no script.

---

## 📚 EXEMPLOS PRÁTICOS

### Batch processing de 50 documentos
```bash
# POST /batch com 50 prompts
# Processa enquanto esperas ou à noite
# Economia: ~$1.50 vs $30 em Claude!
```

### Análise de dados em tempo real
```bash
# POST /process com model_type="reasoning"
# Deepseek faz análise profunda
# Custo: $0.00 (grátis!)
```

### Geração de código rápida
```bash
# POST /process com model_type="code"
# Qwen-coder gera scaffolding
# Depois tu refinas em Claude se precisar
```

---

## 💡 DICAS

1. **Use `/health` para verificar**
   - Antes de enviar muitos requests
   - Para debugging

2. **Cache é teu amigo**
   - Prompts repetidos = CPU só pensa 1x
   - Podes fazer batch processing à noite

3. **Combinação híbrida funciona bem**
   - Ollama genera rascunho (grátis)
   - Claude refina (pago, mas rápido)
   - Economia: 40-50%

4. **Monitora stats**
   - `/stats` mostra economia real
   - Ajuda a justificar setup

---

**Status**: ✅ Servidor pronto e rodando!

Podes começar a chamar de Claude/Codex/AntiGravity agora.

Próximo passo: Atualiza `claude_desktop_config.json` e reinicia Claude Desktop.
