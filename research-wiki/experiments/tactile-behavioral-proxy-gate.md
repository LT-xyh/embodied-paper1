---
type: experiment
node_id: exp:tactile-behavioral-proxy-gate
title: "Tactile behavioral proxy resource gate"
idea_id: "idea:tactile_behavioral_proxy"
verdict: yes
confidence: medium
date: "2026-09-29"
hardware: "No new hardware for dataset consumption; source data collected with tactile sensors"
duration: "Audit only; no download or experiment"
provenance: "TACTILE_BEHAVIORAL_PROXY_REPORT.md; web audit 2026-09-29"
added: 2026-09-29T02:23:11Z
tags: ["tactile", "behavioral-proxy", "resource-gate"]
---

# Tactile behavioral proxy resource gate

**verdict:** `yes`  ·  **confidence:** `medium`  ·  tests `idea:tactile_behavioral_proxy`

## Metrics
Publicity, license, action trajectories, task structure, offline policy metric, split independence, hardware dependence

## Reasoning
FreeTacMan provides public MIT data/code, synchronized visuo-tactile videos and TCP/gripper trajectories, and policy-learning baselines; a task-disjoint offline action/trajectory proxy is feasible on a small subset, but it cannot establish closed-loop success without a simulator or robot.

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

