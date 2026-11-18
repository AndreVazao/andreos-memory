# ECU Pro Tune — estado persistente — 2026-11-15

## Checkpoint confirmado — Windows CI verde e PR aberto
- Repo: AndreVazao/ecu-pro-tune (público).
- Branch: feature/dashboard-advanced-20261108.
- Commit funcional validado: ff2c609cac0ce0bd1df9b0eab04231ffa8a25671.
- GitHub Actions run #4: 43427809165 — SUCCESS.
- Run URL: https://github.com/AndreVazao/ecu-pro-tune/actions/runs/43427809165.
- Job: Windows / Python 3.11 — todos os 16 passos concluídos com sucesso.
- Testes unitários: 4 passed in 0.02s.
- Compileall, pip check, import smoke test e construção Tk dashboard: PASS.
- PyInstaller: build Windows concluído.
- Smoke test do executável: processo iniciou e permaneceu ativo durante os 8 segundos de verificação.
- Artefacto: ECUProTune-Windows-Python311, ID 14036984205, 53,394,215 bytes.
- SHA-256 do ZIP: d535beb11fb51fb0bd59c5210d902a8d6aff84e03501f181a4bd6ba9abcb19dc.
- Retenção do artefacto: até 2026-11-27T12:46:48Z.
- ZIP contém 2.310 ficheiros e ECUProTune.exe (14,852,596 bytes). Distribuição onedir: manter o conteúdo da pasta junto do EXE.
- PR #1 aberto para main: https://github.com/AndreVazao/ecu-pro-tune/pull/1.
- PR aberto, não merged; GitHub reporta mergeable=true.
- Diff original: 6 commits, 3 ficheiros, 463 adições e 82 remoções; documentação de estado atualizada posteriormente.
- Commit da documentação de estado: 2775fb9929f090f7d446a0e015ab3cd5dc7a0e1e.
- Novo run #6 para esse commit: 43749616835, em execução no último check. Run #5 (PR event) foi cancelado automaticamente pelo concurrency ao ser substituído pelo push do commit seguinte; run #6 é o que deve ser acompanhado.
- Não fazer merge sem autorização explícita.
- CodeRabbit não corre automaticamente neste repo com menos de 10 stars; isso não afeta o CI.
- CI valida build/testes e arranque breve, não valida interação visual prolongada, hardware real, ECU física ou funcionamento em todos os PCs.

## Histórico técnico
- Commit do dashboard: 6d28e3c62f9bc15a2f278fd78254bf441cd1125b.
- Workflow: .github/workflows/windows-ci.yml.
- Commit do workflow: 940c7ecd5c26eb9a4ea1e66935b53cba00a44d65.
- Documentação: docs/DEVELOPMENT_STATUS.md.
- AndreOS Memory checkpoint: 5248d4b41cde1ae749beb0e37eca7834296dd02c (checkpoint inicial CI verde); atualização posterior em curso.
- PC-Vazao-Anjos está offline/indisponível; CI corre em runner Windows hospedado pelo GitHub.
- Local ECU: C:\\ProgramasGodMode\\ecu-pro-tune.
- Local memory: C:\\ProgramasGodMode\\andreos-memory.
- O diretório local não versionado andreos-memory deve continuar preservado.

## Implementado
- GUI ttkbootstrap com Performance/Showcase.
- ProfileManager, ECUManager, Scheduler, RollbackManager, SoundManager, Logger.
- MapEditor, validators e live graph.
- Stage 1 profile/map.
- SoundManager fail-safe: MP3 quando disponível, WAV fallback no Windows e backend ausente não bloqueia a GUI.
- Gerador stdlib de 12 cues WAV fallback, 6 por modo, sem dependência de FFmpeg.
- Novo dashboard na branch: seis métricas, RPM/boost gauges, gráfico rolling, monitor de sistema, navegação para Perfis/Mapas e retorno ao dashboard.
- Atualização do dashboard em intervalo de 400 ms e histórico limitado a 90 amostras.
- Identidade visual azul/ciano/preto/cinza, sem novas dependências.

## Segurança
- Nenhuma escrita física de ECU.
- Nenhum driver de flash.
- Toda a telemetria do dashboard é simulada.
- Futura integração de hardware deve ser isolada e fail-closed por defeito.

## Próximos passos
1. Confirmar run #6 verde e validar os checks associados ao PR #1.
2. Rever PR #1 e aguardar autorização explícita antes do merge em main.
3. Teste visual manual no PC Windows quando estiver disponível.
4. Endurecer installer/FFmpeg.
5. Acrescentar testes de integração.
6. Só depois avaliar adapters de hardware, sem escrita física por defeito.


## Checkpoint adicional — 2026-11-17 — run #6 confirmado verde
- Run #6: 43749616835 — SUCCESS, concluído em 2026-11-15T18:58:29Z.
- Commit validado: 2775fb9929f090f7d446a0e015ab3cd5dc7a0e1e.
- URL: https://github.com/AndreVazao/ecu-pro-tune/actions/runs/43749616835.
- Job Windows / Python 3.11: os 16 passos concluídos com sucesso, incluindo pytest (4 passed), imports, construção Tk, PyInstaller, verificação do EXE, smoke test de arranque e upload do artefacto.
- PR #1 permanece open, merged=false, mergeable=true, mergeable_state=clean; branch feature/dashboard-advanced-20261108 para main.
- PR URL: https://github.com/AndreVazao/ecu-pro-tune/pull/1.
- Não foi feito merge. Exigir autorização explícita do utilizador antes de integrar.
- Run #5 continua classificado como cancelamento automático por concurrency, não falha funcional.
- Próximo gate: revisão final do PR e autorização de merge. Depois avançar para teste visual manual em Windows, robustez do instalador e testes de integração.


## Checkpoint 2026-11-17 — PR #1 merged / fase de integração iniciada
- PR #1 (dashboard avançado + Windows CI) foi integrado na main do ECU Pro Tune.
- Merge commit: aa388679e1ea0510c66ed588d4d313e2cbe7e1ba.
- PR #1 URL: https://github.com/AndreVazao/ecu-pro-tune/pull/1.
- Branch main confirmada nesse merge commit.
- Nova branch criada a partir de main: feature/integration-tests-20261117.
- Hardening implementado em validators, ProfileManager, ECUManager e RollbackManager.
- Novos testes em tests/test_integration_managers.py: round-trip de perfil, proteção path traversal, validação de mapas, extração de arrays, backup/restauro, rejeição NaN/inf/bool e nomes inválidos.
- CI run #18: 44035159971 — SUCCESS; commit 7f1b53e0743f049d5b3929db84ed265d062f782d.
- 20 testes passaram em 0.10s.
- pip check, compileall, imports, construção Tk, PyInstaller, verificação do EXE, smoke test de arranque e upload de artefacto: PASS.
- Artefacto: ECUProTune-Windows-Python311, ID 14306118545, 53,396,254 bytes, SHA-256 2787bc15238657ec9446f691521b03d66438178e976812a553a2e321d1cce510, expira em 2026-12-01T07:00:26Z.
- Commit de documentação na branch: 21b976f2ea67fc48a24b5b05471208574e7e5fab.
- CI push #18 validou o commit de código anterior; o commit de documentação vai disparar nova execução.
- PR #2 ainda não criado neste checkpoint; aguardar CI da atualização documental e abrir PR para main.
- Segurança permanece: sem escrita física ECU, sem driver de flash; qualquer futura integração deve ser isolada e fail-closed.
- Próximos passos: confirmar CI do commit docs, criar PR #2, expandir testes scheduler/logging/ficheiros corrompidos/GUI, endurecer installer e validar visualmente em Windows.


## Checkpoint 2026-11-17 — PR #2 merged / scheduler and logger phase
- PR #2 merged successfully into ECU Pro Tune main.
- PR URL: https://github.com/AndreVazao/ecu-pro-tune/pull/2.
- Merge commit: 0980530a17368c919f07867953e51da3dea649da.
- Main CI after merge: run #21, 44035795100 — SUCCESS.
- New branch: feature/scheduler-logging-tests-20261117.
- Scheduler hardened: validates schedule data, profile references and ISO dates; rejects corrupt JSON without overwriting; writes atomically; isolates callback errors; uses cancelable Event.wait instead of fixed sleep.
- New tests cover schedule append/validation, corrupt file preservation, due/future entries, callback retry behavior, and UTF-8 logging.
- CI run #25: 44035973794 — SUCCESS; commit d699874850daf5de3c290e77384ab65d631ec2b8.
- 29 tests passed in 0.12s.
- Full Windows pipeline PASS: dependency check, compileall, imports, Tk dashboard construction, PyInstaller build, EXE verification, packaged startup, artifact upload.
- Artifact ECUProTune-Windows-Python311 ID 14306798921, 53,398,443 bytes.
- SHA-256 adc45d75bb8930a77fe25fffb083dd999c45b6ae4f1606396807bb46d0b78796; expires 2026-12-01T07:06:49Z.
- Documentation commit in branch: 778521ba9f31872ba9c66d7b2002730b8dbc2590.
- PR #3 to be opened after branch documentation commit CI completes.
- No physical ECU write or flash capability; hardware integration remains out of scope until explicitly designed, isolated, and fail-closed.


## Checkpoint 2026-11-17 — PR #3 merged / Windows installer hardening
- PR #3 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/3.
- Merge commit: 8409dce3b6f1ddcabaa2191a34deb126908ca228.
- New branch: feature/windows-installer-hardening-20261117.
- Installer pinned to validated Python 3.11, validates an existing venv, installs dependencies, runs pip check and import smoke validation.
- FFmpeg is optional and winget installation requires explicit user confirmation; GUI/WAV fallback remains usable without FFmpeg.
- ecu_test.bat validates Python 3.11, pip check, compileall and pytest.
- build_exe.bat aligned with CI, bundles configs/maps and ttkbootstrap/matplotlib resources; cleanup restricted to ECUProTune-specific output subfolders.
- README and docs/WINDOWS_INSTALL.md updated.
- New static tests guard installer/build/test batch scripts.
- CI run #39: 44037045786 — SUCCESS; commit 7f188c64428ccebb9118e19e175f3eedfdf718fb.
- 33 tests passed in 0.15s.
- Full Windows pipeline PASS including PyInstaller, EXE verification, packaged startup and artifact upload.
- Artifact ECUProTune-Windows-Python311 ID 14308435021, 53,396,794 bytes.
- SHA-256: fcf00546f29a068064e3d5a001168a8a4ac21b0eeb83b7c85991aacbb8325be9.
- Expires 2026-12-01T07:15:17Z.
- Development status documentation commit: edb088ca2262126271ddd5fba9e069124b6c96a8; a new CI run will validate this documentation-only change.
- PR #4 to main will be opened after the documentation push CI is green.
- No ECU physical write, flash driver, or hardware programming introduced.


## Checkpoint 2026-11-17 — PR #4 merged / versioned release packaging
- PR #4 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/4.
- Merge commit: ee82b350a6b3bb48915f595389366045082c2ab6.
- Main CI after merge: run #43, 44037630731 — SUCCESS.
- New branch: feature/release-packaging-20261117.
- Initial application version set to 0.1.0, shared by VERSION and src/version.py; test enforces equality and app window shows version.
- Added scripts/package_release.ps1: validates EXE, PyInstaller _internal directory and version; creates versioned ZIP, BUILD-MANIFEST.json and SHA256SUMS.txt.
- Build script and Windows CI invoke the same packager; CI independently verifies archive SHA-256 before uploading release folder.
- Added docs/RELEASE_PACKAGING.md and tests/test_release_packaging.py.
- Release ZIP name: ECUProTune-Windows-Python311-v0.1.0.zip.
- Release ZIP SHA-256: aff9f001f9420342c07aa9e9847cfa451c7d73887bde00f6b94404a75c286740.
- CI run #60: 44038026199 — SUCCESS; commit 5835e0c39c6440417abae4a3d194ed0051ac8647.
- 39 tests passed in 0.18s.
- Full Windows pipeline PASS including PyInstaller, EXE startup, release ZIP creation, SHA-256 validation, and artifact upload.
- GitHub artifact ID 14308052177, 53,129,794 bytes; SHA-256 71c0d617d14891f2e1a0d209e8a3832e27566e228bf24cea9887c42eef03ee55; expires 2026-12-01T07:22:53Z.
- Documentation commit d8dcbc622ff235c5f77b6398a1da412b4f585da1; will trigger another branch CI run.
- PR #5 to be opened after documentation commit CI is green.
- No ECU hardware write path or flash driver introduced.


## Checkpoint 2026-11-17 — PR #5 merged / Windows version resource phase
- PR #5 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/5.
- Merge commit: fc6fd26ade4b5b5c4713c1378d5e0c83d4686a48.
- Main branch confirmed at merge commit; main CI run #63 started after merge.
- New branch: feature/windows-version-metadata-20261117.
- Added scripts/generate_windows_version_info.py to read VERSION and generate a PyInstaller Windows version resource.
- Local build_exe.bat and Windows CI now generate and pass build/windows_version_info.txt through --version-file.
- Release manifest records windows_file_version as well as app semver.
- Tests added for generated version resource syntax, file/product version tuples, workflow wiring, and local build wiring.
- Branch CI run #75: 44038890038 is pending/queued at checkpoint; not yet validated.
- Latest branch commit: 51516dd11e79af1e26d982333c9885d04405d465.
- PR #6 not yet opened; wait for CI green and then create.
- Security scope unchanged: no physical ECU write, no flash driver.

- Development documentation updated on feature/windows-version-metadata-20261117: docs commit 89024b36f0e5d6026d14356e40b315676386912d; release guide commit da246ff32161d400455cd7706fe6482f5698d1aa.
- These documentation commits will trigger a fresh CI run; previous run #75 is not yet confirmed green.


## Checkpoint 2026-11-17 — PR #6 merged / EXE version verification
- PR #6 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/6.
- Merge commit: 872788763e78f3272dd97f7b301d1ba3022408b3.
- PR CI run #78: 44039120682 — SUCCESS; 41 tests passed in 0.20s.
- Branch push CI run #77: 44039079454 — SUCCESS.
- New branch: feature/exe-version-verification-20261117.
- Windows CI now reads the built executable VersionInfo and verifies FileVersion and ProductVersion equal VERSION + ".0".
- Mismatch fails CI before smoke/package/upload steps.
- Added regression test for workflow verification and documentation.
- Latest branch docs commit: cd7d9231579dfd5bea7b0c6cb358339af58684b0.
- PR #7 not yet open; latest docs commit will trigger branch CI.
- Main CI run #79 after PR #6 merge was in progress at last check.


## Checkpoint 2026-11-17 — PR #7 merged / Windows EXE version assertion
- PR #7 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/7.
- Merge commit: 227f73821e7c2d5f261bd9ec8e613de51cbe5c15.
- PR CI run #86: 44040161974 — SUCCESS; 42 tests passed in 0.18s.
- Branch push CI run #85: 44039854917 — SUCCESS.
- New workflow step reads the Windows EXE VersionInfo and verifies FileVersion and ProductVersion both match VERSION + ".0".
- The version assertion passed on the built EXE; package, SHA-256 verification and artifact upload also passed.
- Main CI run #87 after merge is in progress at checkpoint.
- Next proposed branch: feature/release-acceptance-20261117 for CHANGELOG and manual Windows acceptance checklist; no public release/tag until manual user-machine validation.


## Checkpoint 2026-11-17 — release acceptance preparation
- PR #7 merged: https://github.com/AndreVazao/ecu-pro-tune/pull/7.
- Merge commit: 227f73821e7c2d5f261bd9ec8e613de51cbe5c15.
- PR CI run #86: 44040161974 — SUCCESS; 42 tests passed in 0.18s.
- Branch push CI run #85: 44039854917 — SUCCESS.
- Main CI run #87 started after merge; verify status in follow-up if needed.
- New branch: feature/release-acceptance-20261117.
- Added CHANGELOG.md for v0.1.0.
- Added docs/ACCEPTANCE_TEST_WINDOWS.md with 14 manual user-machine cases covering install, Python venv, FFmpeg optional path, dashboard, navigation, maps, backup/restore, local build, EXE file version, ZIP extraction, SHA-256 and safety boundary.
- README and docs/DEVELOPMENT_STATUS.md link to the new release/acceptance docs.
- Development docs commit: 1483c94cd947887a00e51c4eef5df60e7b9d5ad4; acceptance plan commit: 7b54136792ae9586df54e1c7e86c698ad63d85e6.
- Branch CI will validate these documentation updates; PR #8 to be opened after CI green.
- Do not publish public tag/release or claim manual acceptance until all 14 cases are executed on a real Windows user machine.


## Checkpoint 2026-11-17 — PR #8 merged / manual acceptance gate prepared
- PR #8 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/8.
- Merge commit: e6d9d600392c694b3a10d646040216f00d5a0bce.
- PR CI run #93: 44040682445 — SUCCESS.
- Branch push CI run #92: 44040604097 — SUCCESS.
- CHANGELOG.md and docs/ACCEPTANCE_TEST_WINDOWS.md merged into main.
- 14 manual Windows acceptance cases cover clean install, wrong venv, optional FFmpeg, launch/version, dashboard simulation, navigation, map validation, backup/restore, test launcher, local build, EXE version metadata, ZIP extraction, hash verification, and safety boundary.
- README links the release notes and manual test plan.
- Main CI run #94: 44040965817 is in progress after merge; verify before final status.
- No public GitHub Release or tag created.
- Manual acceptance is not claimed complete; it requires a real user Windows machine. The previously noted PC-Vazao-Anjos was offline, so do not infer or claim local manual validation.
- Current safe status: code/packaging CI-validated, pending user-machine manual acceptance before public release.


## Checkpoint 2026-11-18 — independent Windows release integrity verifier
- Main CI run #94: 44040965817 — SUCCESS after PR #8 merge.
- New branch: feature/release-integrity-verifier-20261118.
- Added scripts/verify_release.ps1 to independently validate the release manifest, product/version/platform, Windows file version, ZIP filename, archive size, SHA-256 in both manifest and SHA256SUMS.txt, and required onedir entries (ECUProTune.exe and _internal).
- Windows CI invokes the independent verifier after packaging and before artifact upload.
- Added static tests and documented the command in README and docs/RELEASE_PACKAGING.md.
- Windows CI run #100: 44395319597 — SUCCESS; 44 tests passed in 0.21s.
- PyInstaller build, executable version metadata, startup smoke test, ZIP packaging, independent ZIP verification and upload all passed.
- Release ZIP SHA-256: 9b7156513b9d2526820c65a81d72dbd05dc5c970057941418ecbe110de17bbd2.
- GitHub artifact ID 14471145182, 53,130,269 bytes; artifact digest f60e833192b762d7eba9842508ea6b188f94a31aa37b112fffe5f8da737ba2bf; expires 2026-12-02T20:52:59Z.
- Development status documentation commit: 5af210dc8451562a4290713289382607c0840be4; branch CI will validate docs update.
- PR #9 to be opened after documentation commit CI is green.
- Manual Windows user-machine acceptance remains outstanding; no public tag/release until completed.
- No ECU physical write path or flash driver introduced.


## Checkpoint 2026-11-18 — release ZIP path safety
- PR #9 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/9.
- Merge commit: 6baca49faff34b97d88b2b9c783fd987752ba1bf.
- PR CI run #102: 44396154831 — SUCCESS.
- Main CI run #103: 44396501334 — SUCCESS; 45 tests passed in 0.21s.
- New branch: feature/release-archive-path-safety-20261118.
- Hardened scripts/verify_release.ps1 to reject absolute paths, . and .. path segments, content outside ECUProTune/, and duplicate ZIP entries.
- Verifier confirms non-empty ECUProTune.exe and non-empty PyInstaller _internal contents.
- CI run #107: 44396707008 — SUCCESS; 45 tests passed in 0.21s.
- PyInstaller, EXE version metadata, startup smoke test, release ZIP, independent verification and artifact upload passed.
- Release ZIP SHA-256: 92ca165e0f8dfb554228a5fd68e365fb306297fde9cf5a53404fbfa57d741a1c.
- GitHub artifact ID 14471276293, 53,128,733 bytes; digest 91f6304821a9f39febebaf90287193b18db2f671b99235efb66b269e8f071e5e; expires 2026-12-02T21:00:51Z.
- Development status docs commit ae5a1a2189d79d0b5f2dff0b6d1d3d54620e73ab; CI will validate docs update.
- PR #10 to be opened after docs CI succeeds.
- Manual Windows user-machine acceptance remains outstanding; no public release/tag.
- No ECU physical write path or flash driver introduced.


## Checkpoint 2026-11-18 — Windows acceptance recorder
- PR #10 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/10.
- Merge commit: 5b9dce59f2bec0f5c9176fbd9fa9eaf2aa567391.
- PR CI run #109: 44397532910 — SUCCESS.
- Main CI run #110: 44397930870 — SUCCESS.
- New branch: feature/windows-acceptance-recorder-20261118.
- Added scripts/record_windows_acceptance.ps1 to record all 14 manual Windows acceptance cases as PASS/FAIL/SKIP.
- JSON report captures product version, UTC timestamp, Windows edition/version/build, architecture, PowerShell, Python 3.11 availability, case results and notes.
- Overall PASS requires all 14 PASS; FAIL if any case fails; INCOMPLETE if skipped cases remain without failures.
- README and docs/ACCEPTANCE_TEST_WINDOWS.md explain how to run the recorder.
- CI run #115: 44398214617 — SUCCESS; 46 tests passed in 0.18s.
- Full Windows build, executable metadata, startup smoke, release ZIP, independent archive verification and artifact upload passed.
- Release ZIP SHA-256: 275a871dc5fbc90b1257710236daeb2a8dafe3ddd9c8a950245f0dd83a1e28b4.
- GitHub artifact ID 14471692980, 53,129,769 bytes; digest 4b2de2a29fb668ee401ef774e3f760dd95440647b3deb06970049a82029c2c3f; expires 2026-12-02T21:09:24Z.
- Development docs commit 5a5b6dda4b33d454d634f75108ef886ccefbf37; branch CI will validate this docs-only update.
- PR #11 to open after docs CI succeeds.
- Manual acceptance remains pending on a real Windows user machine. Recorder does not execute GUI checks; it only records actual user-entered outcomes.
- No ECU physical write path or flash driver introduced.


## Checkpoint 2026-11-18 — PR #11 merged / structured Windows acceptance recording
- PR #11 merged into main: https://github.com/AndreVazao/ecu-pro-tune/pull/11.
- Merge commit: f72307e2875ac60f4bec84229634a54d7f0af363.
- PR CI run #117: 44399033395 — SUCCESS; 46 tests passed in 0.22s.
- Main CI run #118: 44399399468 was in progress at merge checkpoint.
- scripts/record_windows_acceptance.ps1 prompts for PASS/FAIL/SKIP for all 14 manual Windows cases and writes a structured JSON report.
- Report captures version, UTC timestamp, Windows edition/version/build, architecture, PowerShell version, Python 3.11 availability, per-case outcomes and notes.
- The recorder does not execute GUI checks. Manual acceptance must be performed on a real Windows machine and all 14 cases must be PASS before declaring accepted.
- docs/DEVELOPMENT_STATUS.md updated on main (commit dff639c562bf788db8c2cc59c49c597872c0e96f).
- No public GitHub Release/tag created.
- No ECU physical write path or flash driver introduced.
