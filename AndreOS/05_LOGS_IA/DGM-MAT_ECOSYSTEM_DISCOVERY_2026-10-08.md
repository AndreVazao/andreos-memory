# DGM-MAT Ecosystem Discovery — 2026-10-08

Implemented the first reusable Ecosystem Discovery / Reuse Intelligence boundary in DGM-MAT.

Commit: 759958e5d452dad627f4433ecd27d14c3b79d7a5

Added:
- core/organization/ecosystem_discovery.py
- tests/organization/test_ecosystem_discovery.py
- organization exports
- docs/DGM-MAT_ECOSYSTEM_DISCOVERY.md

Behavior:
- scans approved local roots through the existing non-executing LocalSourceDiscovery
- classifies local/Lab sources
- ranks capability matches by fit, trust, safety and adaptation cost
- reports overlap clusters to reduce accidental duplication
- keeps discovery separate from snapshot/adaptation/promotion
- integrates conceptually with CapabilityRequest, RecruitmentEngine and SkillForge

Validation:
10 organization tests passed.

Safety:
No discovered source is imported or executed by the discovery engine.
No source was auto-promoted.
