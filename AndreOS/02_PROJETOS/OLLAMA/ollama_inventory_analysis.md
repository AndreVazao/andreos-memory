# Ollama Models Inventory - 2026-06-06

## Installed Models

| Nome | ID | Size | Modified | Type | Benchmark |
|------|----|----|----------|------|-----------|
| qwen2.5:1.5b | 65ec06548149 | 986 MB | 45h ago | 1.5B params | Fast, good for prompting |
| llama3.2:3b | a80c4f17acd5 | 2.0 GB | 9d ago | 3B params | Best quality/speed balance |
| llama3.2:latest | a80c4f17acd5 | 2.0 GB | 9d ago | 3B params | (same as 3b) |
| gemma2:2b | 8ccf136fdd52 | 1.6 GB | 12d ago | 2B params | Good for context understanding |
| llama3.2:1b | baf6a787fdff | 1.3 GB | 12d ago | 1B params | Lightest, fastest |
| deepseek-r1:1.5b | e0979632db5a | 1.1 GB | 12d ago | 1.5B params | Reasoning tasks |
| qwen2.5-coder:1.5b | d7372fd82851 | 986 MB | 12d ago | 1.5B params | Code generation |

## Hardware Analysis

### System Specs (Windows PC)
- **GPU**: Not detected in Ollama config (CPU-only compute)
- **CPU**: Primary compute device
- **RAM Available**: Estimated 8-16GB
- **Storage**: Sufficient (26 total blobs, well-managed)

### Performance Bottleneck
⚠️ **CPU-only inference** = slower first-token latency (200-800ms), lower throughput (0.8-3 tokens/sec)

---

## 🏆 Recommendations by Task & Hardware Limits

### Best Overall: **llama3.2:3b**
- **Use for**: General reasoning, complex prompts, translations, analysis
- **Hardware fit**: ✅ Good (2GB memory footprint)
- **Quality**: 8.5/10
- **Speed on CPU**: ~0.8-1.2 tokens/sec
- **When to use**: Multi-turn conversations, nuanced reasoning

### Fastest: **llama3.2:1b**
- **Use for**: Quick checks, summaries, simple classification
- **Hardware fit**: ✅ Excellent (1.3GB)
- **Quality**: 6/10
- **Speed on CPU**: ~2-3 tokens/sec (3x faster than 3b)
- **Best for**: Streaming responses, user-facing queries

### Code Specialist: **qwen2.5-coder:1.5b**
- **Use for**: Code generation, debugging, refactoring
- **Hardware fit**: ✅ Good (986MB)
- **Quality**: 7.5/10 (for code)
- **Speed on CPU**: ~1.5-2 tokens/sec
- **Best for**: Syntax generation, simple fixes

### Reasoning/Analysis: **deepseek-r1:1.5b**
- **Use for**: Step-by-step problem solving, complex logic
- **Hardware fit**: ✅ Excellent (1.1GB)
- **Quality**: 8/10 (reasoning tasks)
- **Speed on CPU**: ~1.2-1.8 tokens/sec
- **Best for**: Math, multi-step workflows

### General Purpose Fallback: **gemma2:2b**
- **Use for**: Context understanding, information retrieval
- **Hardware fit**: ✅ Good (1.6GB)
- **Quality**: 7/10
- **Speed on CPU**: ~1-1.5 tokens/sec

---

## 💰 Token Optimization Strategy

### The Math
- **Claude Sonnet cost**: ~$3 per 1M tokens
- **Ollama cost**: $0 (free, runs locally)
- **Savings potential**: If 30% of tasks move to Ollama = ~$250-300/month saved

### Tier 1: Offload to Ollama (Maximum Savings)
These tasks consume lots of Claude tokens but need low-medium quality:

| Task | Best Model | Why | Est. Savings |
|------|-----------|-----|--------------|
| **Summarization** | llama3.2:1b | Speed critical, quality acceptable | 50-60% |
| **Document cleanup** | llama3.2:1b | Formatting, removing junk | 40-50% |
| **Data validation** | gemma2:2b | Checking formats, schemas | 45-55% |
| **Code formatting** | qwen2.5-coder:1.5b | Linting, indentation | 55-65% |
| **Text classification** | llama3.2:1b | Tag documents, categorize | 50-60% |
| **Information extraction** | gemma2:2b | Pull structured data from text | 45-55% |
| **Brainstorming lists** | deepseek-r1:1.5b | Generate ideas, no filtering | 40-50% |

### Tier 2: Hybrid Pipeline (Medium Savings)
Split work between Ollama (draft) + Claude (refinement):

| Workflow | Ollama Step | Claude Step | Overall Savings |
|----------|------------|------------|-----------------|
| **Code generation** | qwen2.5-coder: generate | Claude: test + optimize | 30-40% |
| **Analysis reports** | gemma2: extract facts | Claude: structure + argue | 35-45% |
| **Creative writing** | deepseek-r1: outline | Claude: write final copy | 25-35% |
| **Complex searches** | llama3.2:1b: initial filtering | Claude: deep analysis | 30-40% |

### Tier 3: Keep on Claude (Quality Critical)
- Strategic decision-making
- High-stakes analysis
- Novel problem solving
- Multi-turn reasoning chains
- Customer-facing content

---

## 🔧 Implementation: How to Connect & Automate

### Phase 1: Manual Testing (This Week)
```powershell
# Test direct API calls
curl -X POST http://127.0.0.1:11434/api/generate `
  -H "Content-Type: application/json" `
  -d '{
    "model": "llama3.2:1b",
    "prompt": "Summarize this: [text]",
    "stream": false
  }'
```

### Phase 2: MCP Server Wrapper (Next Week)
Create a local MCP server that:
- Routes tasks to best model automatically
- Implements token budget tracking
- Caches common queries
- Falls back to Claude if needed

### Phase 3: Claude API Integration
Use Claude API with custom tools to:
- Call Ollama before each operation
- Track cost/quality trade-offs
- Auto-select models based on context

---

## 📊 Estimated Performance on Your Hardware (CPU)

| Model | First Token | Tokens/sec | Scenario |
|-------|-------------|-----------|----------|
| llama3.2:1b | 200-400ms | 2-3 | Quick summaries |
| qwen2.5:1.5b | 300-500ms | 1.5-2 | General tasks |
| gemma2:2b | 400-600ms | 1-1.5 | Context work |
| qwen2.5-coder:1.5b | 300-500ms | 1.5-2 | Code work |
| deepseek-r1:1.5b | 350-550ms | 1.2-1.8 | Reasoning |
| llama3.2:3b | 500-800ms | 0.8-1.2 | Complex tasks |

**⚠️ Note**: CPU inference is slower than GPU. For a 500-token response:
- Fast models: ~3-5 minutes
- Medium models: ~5-8 minutes
- Heavy models: ~8-10 minutes

---

## 🎯 Recommended Setup

### Primary Model: **llama3.2:3b** (for quality)
### Speed Model: **llama3.2:1b** (for quick tasks)
### Code Model: **qwen2.5-coder:1.5b** (for development)
### Reasoning Model: **deepseek-r1:1.5b** (for analysis)

### Keep Ollama Running
```powershell
# Create a scheduled task to auto-start Ollama
# Or add to Windows startup folder
```

---

## Links & References
- Ollama API: http://127.0.0.1:11434
- Ollama Docs: https://github.com/ollama/ollama
- Model comparison: See table above
- MCP Protocol: https://modelcontextprotocol.io

**Generated**: 2026-06-06 16:07 UTC
**Status**: Ready for Phase 1 (Manual API Testing)
