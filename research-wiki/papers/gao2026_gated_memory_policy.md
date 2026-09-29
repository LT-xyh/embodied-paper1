---
type: paper
node_id: paper:gao2026_gated_memory_policy
title: "Gated Memory Policy"
authors: ["Yihuai Gao", "Jeff Jinyun Liu", "Shuang Li", "Shuran Song"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2604.18933"
  doi: null
  s2: null
tags: ["memory", "policy"]
added: 2026-09-29T01:39:56Z
---

# Gated Memory Policy

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

> Robotic manipulation tasks exhibit varying memory requirements, ranging from Markovian tasks that require no memory to non-Markovian tasks that demand in-context memorization of historical information within a single trial or in-context adaptation based on the outcomes of multiple past trials. Surprisingly, simply extending observation histories of a visuomotor policy often leads to a significant performance drop due to distribution shift and overfitting. To address these issues, we propose Gated Memory Policy (GMP), a visuomotor policy that learns both when to recall memory and what to recall. To learn when to recall memory, GMP employs a learned memory gate mechanism that selectively activates history context only when necessary, improving robustness and reactivity. To learn what to recall efficiently, GMP introduces a lightweight cross-attention module that constructs effective latent memory representations. To further enhance robustness, GMP injects diffusion noise into historical actions, mitigating sensitivity to noisy or inaccurate histories during both training and inference. On our proposed non-Markovian benchmark MemMimic, GMP achieves a 30.1% average success rate improvement over long-history baselines, while maintaining competitive performance on Markovian tasks in RoboMimic. All code, data and in-the-wild deployment instructions are available on our project website https://gated-memory-policy.github.io/.

