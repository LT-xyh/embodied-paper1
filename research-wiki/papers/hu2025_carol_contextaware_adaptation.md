---
type: paper
node_id: paper:hu2025_carol_contextaware_adaptation
title: "CARoL: Context-aware Adaptation for Robot Learning"
authors: ["Zechen Hu", "Tong Xu", "Xuesu Xiao", "Xuan Wang"]
year: 2025
venue: "arXiv"
external_ids:
  arxiv: "2506.07006"
  doi: null
  s2: null
tags: ["context", "adaptation"]
added: 2026-09-29T01:39:55Z
---

# CARoL: Context-aware Adaptation for Robot Learning

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

> Using Reinforcement Learning (RL) to learn new robotic tasks from scratch is often inefficient. Leveraging prior knowledge has the potential to significantly enhance learning efficiency, which, however, raises two critical challenges: how to determine the relevancy of existing knowledge and how to adaptively integrate them into learning a new task. In this paper, we propose Context-aware Adaptation for Robot Learning (CARoL), a novel framework to efficiently learn a similar but distinct new task from prior knowledge. CARoL incorporates context awareness by analyzing state transitions in system dynamics to identify similarities between the new task and prior knowledge. It then utilizes these identified similarities to prioritize and adapt specific knowledge pieces for the new task. Additionally, CARoL has a broad applicability spanning policy-based, value-based, and actor-critic RL algorithms. We validate the efficiency and generalizability of CARoL on both simulated robotic platforms and physical ground vehicles. The simulations include CarRacing and LunarLander environments, where CARoL demonstrates faster convergence and higher rewards when learning policies for new tasks. In real-world experiments, we show that CARoL enables a ground vehicle to quickly and efficiently adapt policies learned in simulation to smoothly traverse real-world off-road terrain.

