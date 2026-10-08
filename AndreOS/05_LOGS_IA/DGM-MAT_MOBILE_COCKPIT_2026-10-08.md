# DGM-MAT Mobile Cockpit & Hardware Reality Check — 2026-10-08

## Decision

The mobile dashboard is a first-class DGM-MAT cockpit and must feel like a continuous ChatGPT-style conversation.

Required behavior:

- persistent thread history;
- new conversation;
- rename;
- automatic initial title suggestion;
- project/repository context;
- intent understanding;
- inline state;
- offline queue;
- automatic replay after reconnect.

## Architecture

MOBILE PWA -> VERCEL DISCOVERY -> TAILSCALE -> DGM-MAT PC

Vercel is control-plane/rendezvous only.

Tailscale is private transport.

DGM-MAT PC is execution authority and conversation source of truth.

DGM-MAT-Mobile owns the PWA UI.

DGM-MAT owns the conversation runtime.

## Reuse

Legacy devops-god-mode contains substantial prior cockpit work and is treated as a capability source, not a runtime dependency.

DGM-Cockpit-Frontend is empty and was not imported.

Useful legacy concepts were rebuilt natively under DGM-MAT:

- continuous conversation;
- rename;
- offline queue;
- runtime state;
- Ollama resource policy;
- mobile pairing direction.

## Hardware evidence

Current PC:

- Fujitsu Siemens ESPRIMO Mobile V6535;
- 2 logical CPUs;
- ~3.0 GB RAM;
- Tailscale 1.102.4;
- current Tailscale IPv4: 100.69.225.47;
- DNS: pc-vazao-anjos.taild7e42f.ts.net;
- Tailscale Serve is currently disabled by tailnet policy and needs one-time administrator approval.

Ollama:

- installed at the local Windows user profile;
- server is not kept running on the weak PC;
- installed models include qwen2.5:1.5b, qwen2.5-coder:1.5b, deepseek-r1:1.5b, llama3.2:1b/3b, gemma2:2b;
- real qwen2.5:1.5b generation test failed because model needed ~990.7 MiB and only ~831.7 MiB was available.

Policy:

Do not load local models when available RAM is below the safety threshold.

Future stronger PC should re-benchmark and automatically promote suitable local models.

## Implementation

DGM-MAT added:

- core/mobile_runtime/models.py
- core/mobile_runtime/store.py
- core/mobile_runtime/intent.py
- core/mobile_runtime/service.py
- mobile API endpoints
- mobile PWA static serving
- CORS for remote cockpit
- low-memory local-LLM guard

DGM-MAT-Mobile added the PWA.

DGM-MAT-Deploy added minimal public node discovery without exposing the rendezvous secret.

## Validation

Focused regression:

14 tests passed.

JavaScript syntax check passed.

Python compile check passed.

Local API smoke test passed:

- /mobile/status;
- create thread;
- append message;
- intent classification;
- durable two-message conversation.

## Next

- enable Tailscale Serve;
- publish DGM-MAT-Mobile through Vercel;
- register HTTPS endpoint;
- test phone cockpit;
- connect intent results to mission/orchestrator execution;
- continue reuse discovery with evidence and provenance.

## Vercel publication

The mobile PWA is now linked to Vercel project dgm-mat-mobile with automatic GitHub main deployments.

Latest deployment:
- commit: 654d567313eb434a2204d9e3fb9b13f2a0f00009
- state: READY
- domain: dgm-mat-mobile.vercel.app
- Vercel SSO protection: disabled

The rendezvous deployment also includes public mobile discovery and is READY on production commit 2ad483741d692b083d08248d194062b4160bf96c.

## Heartbeat

DGM-MAT API now refreshes rendezvous registration every 60 seconds with TTL 180 seconds. Public discovery was tested successfully and returned the current PC endpoint.

## Remaining external prerequisite

Tailscale Serve is still disabled by tailnet policy. The one-time administrator approval is required before the HTTPS endpoint can proxy localhost:8181.

Until that approval, the mobile PWA remains correctly designed for offline/local cache and will not claim live PC connectivity.

## Governed mission bridge

Mobile operational intents that are non-destructive and do not require approval now become DGM-MAT missions and enter the existing SafeActionQueue.

Approval-bound intents are not auto-approved by the mobile layer.

Implementation commit: 6740e3b.
