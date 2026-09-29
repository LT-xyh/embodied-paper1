---
type: paper
node_id: paper:yu2026_benchmarking_visionlanguageaction_models
title: "Benchmarking Vision-Language-Action Models on SO-101: Failure and Recovery Analysis"
authors: ["Yi Yu", "Xinchuan Qiu"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2606.08881"
  doi: null
  s2: null
tags: ["evaluation", "failure", "recovery"]
added: 2026-09-29T01:39:51Z
---

# Benchmarking Vision-Language-Action Models on SO-101: Failure and Recovery Analysis

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

> Vision-Language-Action (VLA) models have demonstrated strong generalization in robotic manipulation, yet existing evaluations are primarily conducted in simulation or on expensive robotic platforms, leaving their robustness on affordable real-world robots largely unexplored. We present a standardized real-world benchmark for evaluating representative VLA and imitation learning policies on the low-cost SO-101 robotic platform. The benchmark comprises four representative manipulation tasks together with unified evaluation protocols, enabling systematic comparison under embodiment uncertainty. Using real-world teleoperated demonstrations, we fine-tune and evaluate $π_{0.5}$, SmolVLA, Wall-X, and ACT directly on the physical platform. Beyond conventional task success rates, the benchmark incorporates a structured failure taxonomy, semantic- and execution-level failure decomposition, and recovery-aware evaluation metrics to characterize policy robustness. Experimental results show that stronger pretrained VLA policies generally outperform the imitation learning baseline, although performance remains highly task-dependent under low-cost robotic deployment conditions. Execution instability emerges as the dominant failure source, while recovery capability varies substantially across architectures. These results highlight the importance of failure and recovery analysis beyond binary task success and establish SO-101 as a practical benchmark for evaluating embodied AI systems under realistic low-cost robotic deployment conditions.

