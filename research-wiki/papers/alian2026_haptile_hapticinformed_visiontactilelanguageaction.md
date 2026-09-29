---
type: paper
node_id: paper:alian2026_haptile_hapticinformed_visiontactilelanguageaction
title: "HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning"
authors: ["Amirhosein Alian", "Yongqiang Zhao", "Shiyi Gu", "Xuyang Zhang", "Zhuo Chen", "Christopher E. Mower", "Haitham Bou-Ammar", "Shan Luo"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2606.04825"
  doi: null
  s2: null
tags: ["tactile", "multimodal", "dataset"]
added: 2026-09-29T01:39:48Z
---

# HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning

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

> Despite the importance of tactile sensing for reliable manipulation, most existing Vision-Language-Action (VLA) datasets remain vision-only, and those that do incorporate tactile information typically lack the joint combination of task diversity, language conditioning, and action trajectories. Furthermore, existing teleoperation pipelines rarely provide haptic feedback to the operator, despite its established role in demonstration quality and manipulation stability. In this work, we present HapTile, a contact-grounded visuotactile manipulation dataset that advances beyond vision-only trajectory datasets by embedding physical interaction sensing at two levels: fingertip tactile feedback at the robot end-effector, and haptic-informed demonstrations at the teleoperator side. The data collection platform integrates haptic feedback directly into the teleoperation controller, enabling the operator to perceive contact interactions in real time. It is built around a standard and reproducible robotic system equipped with custom-designed fingertip tactile sensors. The dataset comprises everyday manipulation tasks spanning a broad range of contact-rich skills, including pick-and-place, folding, pressing, stacking, and other routine activities. Each task is paired with language instructions that condition the policy on the manipulation objective, together with synchronized visuotactile observations and action trajectories. In addition, we provide a benchmarking study on contact-rich policy learning using two baseline models to evaluate the effectiveness of the proposed contact-grounded dataset. The dataset and additional details are available on our website: haptile-dataset.github.io.

