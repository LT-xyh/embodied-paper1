---
type: paper
node_id: paper:ji2026_vane_reliable_testtime
title: "VANE: Reliable Test-Time Training for Vision-Language-Action Models"
authors: ["Hongjin Ji", "Guoyang Xia", "Luoyang Sun", "Fangxiang Feng", "Lei Ren"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2608.09448"
  doi: null
  s2: null
tags: ["inference-time", "adaptation"]
added: 2026-09-29T01:39:45Z
---

# VANE: Reliable Test-Time Training for Vision-Language-Action Models

## One-line thesis
Prior work relevant to the current VLA problem-space map; exact thesis to be refined from metadata and paper evidence.

## Problem / Gap
_TODO._

## Method
_TODO._

## Key Results
_TODO._

## Assumptions
_TODO._

## Limitations / Failure Modes
_TODO._

## Reusable Ingredients
_TODO._

## Open Questions
_TODO._

## Claims
_TODO._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
_TODO._

## Abstract (original)

> Test-time training (TTT) offers a lightweight way to adapt vision--language--action (VLA) policies from unlabeled deployment streams, but it remains difficult to use reliably in closed-loop manipulation. A shared adaptation space can mix incompatible task corrections, while an online update can alter subsequent actions before its consequences are known. We introduce a reliable TTT framework for VLA policies (VANE). VANE conditions prompt adaptation on the current vision--language context and learns from the future visual consequences of executed actions. Candidate updates are isolated from the live policy, evaluated on subsequent observations, and committed only when supported by future evidence, making adaptation selective and reversible. On SimplerEnv WidowX, VANE improves average success by $3.2$ percentage points over the corresponding TTT baseline. Results on Google Robot further show that deployment-time gains remain task- and embodiment-dependent. Together, these results demonstrate a constrained, evidence-based approach to adapting VLA policies during interaction.

