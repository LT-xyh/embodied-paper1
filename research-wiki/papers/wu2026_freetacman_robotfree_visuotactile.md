---
type: paper
node_id: paper:wu2026_freetacman_robotfree_visuotactile
title: "FreeTacMan: Robot-free Visuo-Tactile Data Collection System for Contact-rich Manipulation"
authors: ["Longyan Wu", "Checheng Yu", "Jieji Ren", "Li Chen", "Yufei Jiang", "Ran Huang", "Guoying Gu", "Hongyang Li"]
year: 2026
venue: "ICRA 2026"
external_ids:
  arxiv: "2506.01941"
  doi: null
  s2: null
tags: ["tactile", "visuo-tactile", "action-trajectories", "imitation-learning", "dataset"]
added: 2026-09-29T02:23:11Z
---

# FreeTacMan: Robot-free Visuo-Tactile Data Collection System for Contact-rich Manipulation

## One-line thesis
Public visuo-tactile manipulation trajectories support action-conditioned imitation learning without requiring new tactile hardware for dataset consumption.

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

> Enabling robots with contact-rich manipulation remains a pivotal challenge in robot learning, which is substantially hindered by the data collection gap, including its inefficiency and limited sensor setup. While prior work has explored handheld paradigms, their rod-based mechanical structures remain rigid and unintuitive, providing limited tactile feedback and posing challenges for operators. Motivated by the dexterity and force feedback of human motion, we propose FreeTacMan, a human-centric and robot-free data collection system for accurate and efficient robot manipulation. Concretely, we design a wearable gripper with visuo-tactile sensors for data collection, which can be worn by human fingers for intuitive control. A high-precision optical tracking system is introduced to capture end-effector poses while synchronizing visual and tactile feedback simultaneously. We leverage FreeTacMan to collect a large-scale multimodal dataset, comprising over 3000k paired visuo-tactile images with end-effector poses, 10k demonstration trajectories across 50 diverse contact-rich manipulation tasks. FreeTacMan achieves multiple improvements in data collection performance over prior works and enables effective policy learning from self-collected datasets. By open-sourcing the hardware and the dataset, we aim to facilitate reproducibility and support research in visuo-tactile manipulation.

