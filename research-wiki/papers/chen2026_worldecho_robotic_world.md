---
type: paper
node_id: paper:chen2026_worldecho_robotic_world
title: "WorldEcho: Do Robotic World Models Really Follow Actions?"
authors: ["Sixiang Chen", "Jiaming Liu", "Jixian Wu", "Yichen Guo", "Tinghao Wang", "Siyuan Qian", "Hao Chen", "Jiajun Cao", "Jian Tang", "Shanghang Zhang"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2608.24885"
  doi: null
  s2: null
tags: ["world-model", "evaluation"]
added: 2026-09-29T01:39:54Z
---

# WorldEcho: Do Robotic World Models Really Follow Actions?

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

> Action-conditioned world models are increasingly used as learned simulators for policy evaluation and improvement, yet their effectiveness rests on an unverified assumption: generated futures faithfully reflect arbitrary valid actions. Existing benchmarks are typically confined to expert demonstrations, leaving off-expert action following inadequately evaluated. To address this gap, we introduce WorldEcho, which probes action following over a broader action distribution using visual integrity and SE(3) trajectory alignment. Our diagnosis shows that current world models reasonably execute expert actions but struggle with diverse off-expert trajectories, either ignoring the commanded actions or producing visually invalid rollouts. We further propose WorldSync, which strengthens action following along three complementary axes: distributional coverage, representational grounding, and intervention-effect alignment. It broadens the training distribution over action consequences, grounds intermediate video representations in action-induced robot dynamics through an Action-Forcing Expert, and aligns predicted changes under action interventions with the corresponding changes in ground-truth futures. Experiments on RoboTwin benchmarks and real-robot tasks show that WorldSync improves WorldEcho metrics and serves as a more reliable simulator for iterative policy improvement, enabling policies to achieve higher success rates.

