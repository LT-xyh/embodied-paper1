---
type: idea
node_id: idea:tactile_behavioral_proxy
title: "Tactile behavioral proxy via FreeTacMan"
stage: proposed
outcome: pending
added: 2026-09-29T02:23:11Z
based_on: ["paper:wu2026_freetacman_robotfree_visuotactile"]
target_gaps: []
tags: ["tactile", "behavioral-proxy", "offline-imitation", "resource-gate"]
---

# Tactile behavioral proxy via FreeTacMan

**stage:** `proposed`  ·  **outcome:** `pending`

Use task-disjoint FreeTacMan visuo-tactile trajectories for held-out action and trajectory-quality evaluation without collecting new tactile data.

## Thesis
A public action-trajectory dataset can test whether tactile input improves behavior-level generalization under task-disjoint evaluation, while separating offline action quality from claims about closed-loop success.

## Key risks
The 50.3 GB release is nontrivial; official task-disjoint splits and a simulator are absent; offline action prediction may not predict closed-loop success.

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

