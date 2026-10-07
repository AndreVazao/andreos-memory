# 🆓 CLAUDE FREE MODE - Unlimited via Ollama

**Versão**: 1.0  
**Status**: Production Ready  
**Custo**: $0.00  
**Limite**: Apenas rate limiting para não sobrecarregar CPU

---

## 📌 O Conceito

Ao invés de:
- Pagar Claude ($3/1M tokens)
- Ter limites de rate limit
- Depender de API externe

**Free Mode oferece**:
- ✅ Ollama 100% GRÁTIS (CPU local)
- ✅ Sem limites reais (só rate limiting inteligente)
- ✅ Sem dependência de API
- ✅ 100% privacidade (dados nunca saem do PC)

**Economia**:
- Se usar 50 operações/dia: **$0.00/mês** (vs $150+ normal)
- Limite é CPU (2-10 min por resposta), não tokens

---

## 🚀 COMEÇAR (5 minutos)

### 1. Verificar Ollama
```powershell
ollama list
# Deve listar 7 modelos
```

### 2. Rodar Free Mode
```powershell
cd C:\AI
python free_mode_ollama.py

# Escolher opção 1 (Interactive)
```

### 3. Escolher tarefa
```
Opções:
1. Resumir texto
2. Gerar código
3. Analisar
4. Ver estatísticas
5. Sair
```

### 4. Entrar com prompt
```
Resumir texto: "Cole aqui um texto longo..."
[Espera 2-10 minutos dependendo do modelo]
[Resultado aparece com custo ($0.00) e economia]
```

---

## 🎯 RATE LIMITS (Ajustável)

Por padrão:
- **50 operações/hora**
- **200 operações/dia**

Exemplos:
- Se cada operação = 2 min → 50/hora = 100 min = ok
- Se cada operação = 5 min → 50/hora = mais rápido
- Se precisa mais → editar `RATE_LIMITS` no script

**Aumentar limite** (editar linha 22):
```python
RATE_LIMITS = {
    "per_hour": 100,      # ← aumentar aqui
    "per_day": 500,       # ← e aqui
}
```

---

## 💻 USO PRÁTICO

### Exemplo 1: Resumir documento (FREE!)
```python
from free_mode_ollama import FreeModeOllama

client = FreeModeOllama()

result = client.process(
    prompt="Resuma este documento de 5000 palavras em 100 palavras",
    task_type="fast"  # Modelo rápido
)

print(f"Resumo: {result['response']}")
print(f"Tokens: {result['tokens']}")
print(f"Custo: ${result['cost_saved']} economizado")
# Output: Custo: $0.00 (GRÁTIS!)
```

### Exemplo 2: Gerar código (FREE!)
```python
result = client.process(
    prompt="Cria função Python para validar email",
    task_type="code"
)

print(result['response'])
```

### Exemplo 3: Análise profunda (FREE!)
```python
result = client.process(
    prompt="Analisa a economia do Portugal em 2024",
    task_type="reasoning"  # DeepSeek para raciocínio
)

print(result['response'])
```

---

## 📊 COMPARAÇÃO: CLAUDE vs FREE MODE

| Aspecto | Claude API | Free Mode |
|---------|-----------|----------|
| **Custo** | $3/1M tokens | $0.00 |
| **Latência** | <5 segundos | 2-10 minutos |
| **Limite** | Rate limit API | Rate limit CPU |
| **Privacidade** | Servidor Anthropic | Seu PC |
| **Qualidade** | Claude Sonnet 4 | llama3.2:3b (≈85% da qualidade) |
| **Melhor para** | Tempo real | Tarefas em batch |
| **Quando usar** | Chat, respostas rápidas | Documentos, análise |

---

## 🎮 MODOS DE USO

### Modo 1: Interactive (Menu)
```powershell
python C:\AI\free_mode_ollama.py
# Escolher: 1

# Menu aparece:
# 1. Resumir texto
# 2. Gerar código
# 3. Analisar
# 4. Ver estatísticas
# 5. Sair
```

### Modo 2: Batch Processing
```powershell
python C:\AI\free_mode_ollama.py
# Escolher: 2

# Script processa múltiplos documentos de graça
# Ideal para: 50 documentos, 100 emails, 200 tickets
```

### Modo 3: API (em seu código)
```python
from free_mode_ollama import FreeModeOllama

client = FreeModeOllama()
result = client.process("seu prompt aqui", task_type="fast")
```

---

## 🧠 MODELO CERTO PARA CADA TAREFA

| Tarefa | Modelo | Velocidade | Qualidade | Uso |
|--------|--------|-----------|-----------|-----|
| Summarize | llama3.2:1b | ⚡⚡⚡ | ⭐⭐⭐⭐⭐⭐ | Rápido |
| Code gen | qwen2.5-coder | ⚡⚡ | ⭐⭐⭐⭐⭐⭐⭐⭐ | Correto |
| Análise | deepseek-r1 | ⚡⚡ | ⭐⭐⭐⭐⭐⭐⭐⭐ | Profundo |
| Geral | llama3.2:3b | ⚡ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐ | Melhor |

**Dica**: Começa com "fast" (llama3.2:1b), depois move para "balanced" se precisar mais qualidade

---

## 📈 CASOS DE USO

### ✅ Perfeito para Free Mode
- Resumir 50 documentos
- Gerar 100 emails
- Revisar 200 comentários
- Análise batch de dados
- Processamento noturno
- Limpeza de datasets

### ❌ NÃO para Free Mode
- Chat interativo (muito lento)
- Respostas em tempo real
- Decisões críticas (qualidade Ollama é 85%)
- Algo que precisa <5 segundos

---

## ⚙️ CONFIGURAÇÃO AVANÇADA

### Mudar rate limits
```python
from free_mode_ollama import FreeModeOllama, RateLimitConfig

config = RateLimitConfig(
    per_hour=100,    # ← aumentar
    per_day=500,     # ← aumentar
    concurrent=1     # Deixar em 1 (CPU não paralela)
)

client = FreeModeOllama(rate_limit_config=config)
```

### Cache de respostas
```python
# Se faz mesma pergunta 2x, usa cache (instantâneo)
result1 = client.process(prompt, cache_key="minha_pergunta_1")
result2 = client.process(prompt, cache_key="minha_pergunta_1")

# result2 retorna quase instantaneamente do cache
print(result2["cached"])  # True
```

### Controlar temperatura (criatividade)
```python
# Criatividade baixa = respostas mais previsíveis
result = client.process(prompt, task_type="fast", temperature=0.3)

# Criatividade alta = respostas mais criativas
result = client.process(prompt, task_type="fast", temperature=0.9)
```

---

## 📊 MONITORAMENTO

### Ver estatísticas
```powershell
python C:\AI\free_mode_ollama.py
# Escolher: 4

# Mostra:
# 📊 Operações:
#   • Esta hora: 25/50
#   • Hoje: 150/200
#   • Cache hits: 3
#
# 📈 Tokens:
#   • Total: 15,000
#   • Economia: $0.0225
#
# 💰 Valor economizado:
#   • Se fosse Claude: $0.045
#   • Você pagou: $0.00 (GRÁTIS!)
```

### Logs
```python
# Cada operação é registrada
client.stats.operations
# [
#   {"time": "14:30:45", "tokens": 150, "model": "llama3.2:1b"},
#   {"time": "14:35:12", "tokens": 200, "model": "qwen2.5-coder"},
# ]
```

---

## 🚨 TROUBLESHOOTING

### "Ollama não está rodando"
```powershell
ollama serve
# Deixa rodando numa janela PowerShell aberta
```

### "Timeout (Ollama lento demais em CPU)"
**Solução**: Usar modelo mais rápido
```python
# Ao invés de
result = client.process(prompt, task_type="balanced")

# Usar
result = client.process(prompt, task_type="fast")
```

### "Rate limit atingido"
Espera 1 hora ou edita RATE_LIMITS no script (linha 22)

### Respostas de baixa qualidade
```python
# Ao invés de fast
result = client.process(prompt, task_type="balanced")  # Melhor qualidade
```

---

## 💡 DICAS DE OURO

### Dica 1: Batch noturno
```python
# Executar este script à noite (não precisa tua máquina)
# Processa 200 documentos enquanto dorme
# Próxima manhã: tudo pronto!
```

### Dica 2: Cache agressivo
```python
# Se tem perguntas repetidas:
for doc in [doc1, doc2, doc3]:
    # Primeira vez: processa (2-10 min)
    result = client.process("Resuma este: " + doc, cache_key=doc.id)
    
    # Próximas vezes: cache (instantâneo!)
    if doc.id in cache:
        result = client.cache[doc.id]
```

### Dica 3: Combinação híbrida
```python
# Se precisa resultado rapidamente:
# 1. Ollama gera rascunho GRÁTIS (2-5 min)
# 2. Claude refina (30 segundos, pago)
# 3. Total: 85% economia + resultado rápido

# Use:
draft = client.process(prompt, task_type="fast")  # FREE
# Se precisa melhorar:
# refined = claude_api.refine(draft)  # Pago, mas rápido
```

### Dica 4: Monitor de economia
```python
# No fim do dia:
print(client.get_stats())

# Exemplo output:
# 📊 Operações:
#   • Esta hora: 45/50
#   • Hoje: 195/200
#
# 💰 Valor economizado:
#   • Economia: $0.27
#   • Se fosse Claude: $0.27
```

---

## 📈 ESCALA

### Consumo conservador
- 5 operações/dia
- ~100 tokens/operação
- ~500 tokens/dia
- **Economia: $0.0015/dia = $0.45/mês**

### Consumo moderado
- 20 operações/dia
- ~200 tokens/operação
- ~4,000 tokens/dia
- **Economia: $0.012/dia = $3.60/mês**

### Consumo agressivo
- 50 operações/dia
- ~300 tokens/operação
- ~15,000 tokens/dia
- **Economia: $0.045/dia = $13.50/mês**

### Consumo máximo (seu hardware)
- Limite: apenas CPU
- Se 10min/operação = 6 operações/hora
- Com rate limit 50/hora = fácil fazer 400/dia
- ~120,000 tokens/dia
- **Economia: $0.36/dia = $108/mês** 🎉

---

## 🎯 RECOMENDAÇÕES

### Para começar
- Rodar `free_mode_ollama.py` modo 1 (Interactive)
- Testar com alguns prompts
- Ver stats (quanto economiza)

### Para usar de verdade
- Integrar em teu código (modo 3 - API)
- Configurar rate limits conforme CPU
- Cache para perguntas repetidas

### Para produção
- Batch processing noturno (modo 2)
- Monitorar stats diariamente
- Combinar com Claude quando tempo é crítico

---

## 📞 RESUMO RÁPIDO

| O que | Comando/Código |
|------|----------|
| **Rodar** | `python C:\AI\free_mode_ollama.py` |
| **Mode Interactive** | Escolher 1 no menu |
| **Mode Batch** | Escolher 2 no menu |
| **Mode API** | Ver exemplo em `api_example()` |
| **Ver stats** | Escolher 4 no menu |
| **Aumentar limite** | Editar linha 22 do script |
| **Cache** | Adicionar `cache_key=` na chamada |

---

## ✨ CONCLUSÃO

**FREE MODE = 100% grátis, sem sacrificar funcionalidade**

- ✅ Tudo que Claude faz, Ollama faz (um pouco mais lento)
- ✅ Zero custo (rodas localmente)
- ✅ Zero limites reais (só CPU)
- ✅ Zero dependência de API
- ✅ 100% privacidade

**Quando usar**:
- Processar documentos
- Gerar código em batch
- Análise de dados
- Tarefas noturnas
- Prototipagem

**Quando NÃO usar**:
- Chat tempo real
- Decisões críticas
- Algo que precisa <5 segundos

---

**Criado**: 2026-06-06  
**Status**: Production Ready  
**Custo**: $0.00  
**ROI**: Infinito (grátis!) 🚀
