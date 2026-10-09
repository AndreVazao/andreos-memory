# DGM-MAT — Claude Code CPU compatibility and launcher recovery

Date: 2026-10-09
Device: PC-Vazao-Anjos

## Incident

Desktop shortcuts opened and then appeared to crash/close. Windows Application Error events recorded Claude Code native executable version 2.1.158 failing with exception `0xC000001D` (illegal instruction). The executable's Authenticode signature verified as Anthropic. The machine has an Intel Pentium Dual-Core T3200 (2 cores / 2 threads), Windows 10 Home x64, Node.js 24.20.0, npm 11.16.0.

The failure occurs before authentication or project loading, so repeated reinstallations of the same native binary are not an appropriate fix. Public issue reports document that the native/Bun executable requires CPU instruction features absent from some older CPUs and that the last npm release with a genuine JavaScript `cli.js` fallback is 2.1.112.

## Recovery implemented

- Downloaded `@anthropic-ai/claude-code@2.1.112` from npm into an isolated directory and extracted its package without replacing the original installation.
- Installed path: `C:\ProgramasGodMode\tools\claude-code-node-2.1.112\package\cli.js`.
- Set `DISABLE_AUTOUPDATER=1` in wrappers to protect the compatibility fallback.
- Updated `C:\ProgramasGodMode\ClaudeCode.cmd` and `ClaudeCode-Ollama.cmd` to use the Node-based CLI, keep the console visible after exit, and write logs to `%LOCALAPPDATA%\DGM-MAT\logs\`.
- Corrected the DGM-MAT menu's `if errorlevel` branching so choice 1/2 is not skipped by an unconditional `&` command.
- Updated global `claude.cmd` and `claude.ps1` shims to route `claude` commands through the Node-compatible CLI from any working directory. Original shims were backed up as `*.bak-20261009-085423` under `%APPDATA%\npm`.
- Repaired desktop shortcut `Claude.lnk`, whose target was blank, to open the DGM-MAT Claude Agent menu. Verified the other Claude/DGM-MAT shortcuts point to valid launchers.
- Updated the portable package to include the Node-based CLI and refreshed `DGM-MAT-Claude-Agent-Portable.zip`.

## Validation

- `node cli.js --version` => `2.1.112 (Claude Code)`.
- `ClaudeCode.cmd --version` => version 2.1.112, exit code 0.
- Global `claude --version` in PowerShell => version 2.1.112, exit code 0.
- Global `claude --version` from CMD => version 2.1.112, exit code 0.
- Global command from `C:\Windows\System32` => version 2.1.112, exit code 0, confirming the wrapper works outside the project folder.
- `claude --help` => usage output, exit code 0.
- Portable launcher `ClaudeCode.cmd --version` => version 2.1.112, exit code 0.
- Portable menu exit selection works; ZIP contains the launchers, README, and `tools/claude-code-node-2.1.112/package/cli.js`.

## Important limits / next actions

- Version 2.1.112 is a compatibility pin, not the latest release. Test any upgrade in an isolated folder before replacing this working CLI.
- The native 2.1.158 package remains installed but the global command shims and launchers no longer invoke its incompatible executable.
- Claude authentication/provider connectivity still needs a real interactive session test; `--version` and `--help` prove startup compatibility, not successful model calls.
- Claude Code + Ollama is still experimental and must not be marked functional until a real prompt/response test passes.
- Free Claude Code/FCC, NVIDIA NIM, OmniRoute, Ruflo, and browser automation must each be tested independently. Do not infer that they work because the Claude CLI itself now starts.
- Preserve broad autonomy for reversible work, but require explicit confirmation for destructive/irreversible actions.
