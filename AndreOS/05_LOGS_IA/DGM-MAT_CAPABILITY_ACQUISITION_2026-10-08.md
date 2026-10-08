# DGM-MAT Capability Acquisition & Open Recruitment — 2026-10-08

## Decision

DGM-MAT now has an explicit capability acquisition and open recruitment model.

A missing capability becomes a first-class Capability Request. HQ can discover
existing implementations in local projects, DGM-MAT-Labs, skills-labs, approved
repositories and GitHub, then turn a validated candidate into a DGM-MAT-owned
module and, when justified, recruit a dedicated digital worker.

## Pipeline

REQUEST -> DISCOVER -> ASSESS -> SNAPSHOT -> SANDBOX -> ADAPT -> TEST -> REVIEW -> PROMOTE -> REGISTER -> ACTIVATE

Critical invariant:

**Labs are reuse sources, not runtime dependencies.**

Source code is never blindly imported into DGM-MAT. The source is evidence; the
adapted module is the product; the worker is the employee; tests are the proof;
provenance is the history.

## Implemented

DGM-MAT main now contains:

- capability domain models;
- CapabilityRegistry;
- LocalSourceDiscovery;
- SkillForge staging/adaptation foundation;
- RecruitmentEngine;
- acquisition policy;
- non-destructive organization bootstrap;
- capability acquisition documentation.

PR #70 was merged into DGM-MAT main.

Final validation from a clean worktree:
**8 organization foundation/recruitment tests passed.**

## Local source inventory observed

The PC currently contains reusable skill laboratories around:

- browser automation;
- OpenAI;
- Anthropic;
- Gemini;
- Google Cloud;
- Cloudflare;
- Vercel;
- HeyGen;
- Android/mobile;
- Ollama/local AI;
- Praison;
- Ruflo;
- Smol AI.

A particularly relevant existing lab artifact is a browser-act skill forge inside
the browser skills laboratory. It is treated as a source to evaluate, not as a
runtime dependency.

There are also existing projects such as VocalClaw_11Labs and Lab-OllamaConection
that can become future capability candidates when a mission requires them.

## Reconstruction rule

DGM-MAT-FULL-MIRROR remains immutable archaeology.

The active DGM-MAT is rebuilt from:

1. existing working code;
2. architecture mapping;
3. validated reusable components;
4. Lab/reference candidates;
5. tests and independent review;
6. explicit contracts;
7. provenance and memory.

The objective is not to reproduce the old DGM-MAT. The objective is to preserve
what is valuable while rebuilding the architecture correctly.
