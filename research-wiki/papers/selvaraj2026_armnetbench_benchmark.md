---
type: paper
node_id: paper:selvaraj2026_armnetbench_benchmark
title: "ArmnetBench: A Benchmark for ..."
authors: ["Praveen Selvaraj", "Lorenzo Uttini", "Ville Kuosmanen"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2607.24481"
  doi: null
  s2: null
tags: ["benchmark", "data-quality"]
added: 2026-09-29T01:39:59Z
---

# ArmnetBench: A Benchmark for ...

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

> Real-world evaluation is a bottleneck in developing generalist robot manipulation policies. Each rollout requires physical hardware and an operator to set up, reset, and score it. We introduce ArmnetBench v0.1, a benchmark run on a fleet of low-cost SO-101 cells under light on-site supervision. v0.1 validates this arm farm end to end and compares 7 policies across 12 tasks with both single-arm and bimanual configurations. Each policy is trained or fine-tuned on 50 demonstrations per task; the benchmark contains 2,518 policy rollouts and 600 reference demonstrations. All 3,118 episodes carry a three-way label (successful, suboptimal, or failure). Policy rollouts are human-scored, while demonstrations are successful by construction. Beyond evaluation, its quality-labelled trajectories support downstream learning, from reward and predictive world models to policies trained on mixed-quality data. The leaderboard is an initial comparison under this shared budget. We release the 3,118 core episodes in LeRobot v3.0 and RoboMeter formats.

