# Policy Briefing: Unicode Character Evasion & Text Normalization Guardrails
**Document Reference:** P2-POLICY-2026-A  
**Security Classification:** Core Trust & Safety Operating Standard  

## Executive Summary
Sophisticated bad actors are deploying non-standard typography, mixed character sets (homoglyphs), and hidden spaces to bypass keyword filters. This document sets clear operating standards for character normalization across all commercial platforms, protecting user safety without slowing down system performance.

## Core Policy Requirements
1. **Mandatory Multi-Stage Cleanups:** All text input fields must strip hidden spacing patterns before routing data to validation layers.
2. **Standardizing Character Meanings:** Text elements containing international character sets must be mapped back to base alphabets using standard Unicode rules.
3. **Continuous Accuracy Tracking:** Filter rules must undergo regular validation reviews to catch performance drops before they impact users.
