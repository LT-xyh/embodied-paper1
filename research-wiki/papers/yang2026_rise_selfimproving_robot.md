---
type: paper
node_id: paper:yang2026_rise_selfimproving_robot
title: "RISE: Self-Improving Robot Policy with Compositional World Model"
authors: ["Jiazhi Yang", "Kunyang Lin", "Jinwei Li", "Wencong Zhang", "Tianwei Lin", "Longyan Wu", "Zhizhong Su", "Hao Zhao", "Ya-Qin Zhang", "Li Chen", "Ping Luo", "Xiangyu Yue", "Hongyang Li"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2602.11075"
  doi: null
  s2: null
tags: ["world-model", "self-improvement"]
added: 2026-09-29T01:45:52Z
---

# RISE: Self-Improving Robot Policy with Compositional World Model

## One-line thesis
Recent VLA literature used to map a distinct problem space and its current limitations.

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

> Despite the sustained scaling on model capacity and data acquisition, Vision-Language-Action (VLA) models remain brittle in contact-rich and dynamic manipulation tasks, where minor execution deviations can compound into failures. While reinforcement learning (RL) offers a principled path to robustness, on-policy RL in the physical world is constrained by safety risk, hardware cost, and environment reset. To bridge this gap, we present RISE, a scalable framework of robotic reinforcement learning via imagination. At its core is a Compositional World Model that (i) predicts multi-view future via a controllable dynamics model, and (ii) evaluates imagined outcomes with a progress value model, producing informative advantages for the policy improvement. Such compositional design allows state and value to be tailored by best-suited yet distinct architectures and objectives. These components are integrated into a closed-loop self-improving pipeline that continuously generates imaginary rollouts, estimates advantages, and updates the policy in imaginary space without costly physical interaction. Across three challenging real-world tasks, RISE yields significant improvement over prior art, with more than +35% absolute performance increase in dynamic brick sorting, +45% for backpack packing, and +35% for box closing, respectively.

