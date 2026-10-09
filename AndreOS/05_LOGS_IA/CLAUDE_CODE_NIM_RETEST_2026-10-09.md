# Path: C:\AndreOS-Memory\AndreOS\05_LOGS_IA\CLAUDE_CODE_NIM_RETEST_2026-10-09.md

# Claude Code / FCC / NVIDIA NIM retest — 2026-10-09

## Verified
- Node v24.20.0; npm 11.16.0.
- Claude Code Node-compatible fallback v2.1.112 works for `claude --version`, exit code 0. Primary launcher `C:\ProgramasGodMode\ClaudeCode.cmd --version` also returned v2.1.112, exit code 0, and preserved a visible diagnostic/log path.
- FCC 6.10.4 is active; `DGM-MAT-Ensure-FCC-Server.ps1` exit 0; admin UI `http://127.0.0.1:8082/admin` returned HTTP 200.
- FCC status reported NVIDIA NIM configured/running, selected model `nvidia_nim/nvidia/nemotron-3-super-120b-a12b`, and 80 catalog models.
- A real short `fcc-claude -p --output-format text --max-turns 1` inference returned exactly `NIM_OK`, exit code 0. This verifies one request/response only, not a free-tier guarantee or sustained reliability.
- Five relevant desktop shortcuts have existing targets and working directories.
- Portable ZIP listing succeeded: 30 entries, expected `package/cli.js` and `package/package.json`, SHA-256 `C85C4C9F276996B28824652C00D588670979569BE7E7C3A7996841A6302D1068`. Filename-level scan found no obvious .env/token/secret/credentials files. No second-PC extraction/install test was performed.
- OmniRoute 3.8.51 and Ruflo 3.55.0 respond to version/help checks.

## Not ready / caveats
- Ollama at `127.0.0.1:11434` did not respond; no models were returned. Do not mark local fallback as functional.
- OmniRoute warned that its `.env` is inside the installed npm package and can be replaced by package updates. The file was not read, copied, moved, or changed. Resolve this before updating OmniRoute.
- Longer read-only Claude Code plan-mode/source-review attempts failed to return a useful final report within the configured turn/time budgets. One hit max turns; another ended with exit code 1 and empty output; a longer text query was stopped when it did not complete in the observed window. No repository files were changed.
- Therefore: NIM short inference is proven, but Claude Code's full file-reading/tool-use workflow is NOT yet validated. Do not grant it write permissions or trust it for autonomous code changes until a bounded read-only review returns a useful report and exits cleanly.
- The inventory detected 37 browser-skill folders; that is discovery only, not 37 successful functional tests.

## Safe usage plan
1. Keep the short `NIM_OK` smoke test as a minimal provider test.
2. Continue having ChatGPT prepare/verify source changes. Use FCC/NIM only for short secondary opinions that do not require file tools until tool-use is diagnosed.
3. Diagnose Claude Code plan-mode/tool-call/turn behavior before treating it as an operational DGM-MAT subagent.
4. Resolve OmniRoute config location safely before package updates, without printing secret values.
5. Restart/test Ollama separately and verify a real local inference before considering it a fallback.

Detailed report:
`C:\ProgramasGodMode\DGM-MAT-Agent-Reports\2026-10-09-provider-audit\CLAUDE-CODE-NIM-RETEST.md`

Safety: no credential values displayed or changed; no adapters activated; no source code changed during this retest.
