---
type: paper
node_id: paper:tao2026_foretacvla_forecastingbased_tactilevisionlanguageaction
title: "ForeTac-VLA: A Forecasting-Based Tactile-Vision-Language-Action Model for Contact-Rich Robotic Manipulation"
authors: ["Zhengyu Tao", "Xin Li", "Xin Wang"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2609.20980"
  doi: null
  s2: null
tags: ["tactile", "forecasting", "VLA"]
added: 2026-09-29T01:39:49Z
---

# ForeTac-VLA: A Forecasting-Based Tactile-Vision-Language-Action Model for Contact-Rich Robotic Manipulation

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

> Vision-language-action (VLA) models have demonstrated strong capabilities in robotic manipulation, yet their reliance on visual perception limits robustness in contact-rich environments, where critical physical interaction states may not be visually observable. Existing tactile-enhanced VLA methods improve physical grounding using observed tactile feedback, but most remain largely reactive rather than explicitly modeling how contact may evolve. Therefore, we propose ForeTac-VLA, a forecasting-based tactile-vision-language fusion model that predicts future tactile states to guide action generation. Specifically, ForeTac-VLA encodes recent tactile observations into temporal representations and integrates them with vision-language features through bidirectional cross-attention. Further, a transformer-based forecasting module predicts multi-step future tactile states, enabling the model to reason jointly over observed and anticipated contact. Finally, the fused multimodal representations and predicted future tactile states are fed into the VLA backbone to condition action generation. To stabilize training, a ground-truth-to-prediction curriculum is employed when early forecasts are unreliable. Across four real-world contact-rich manipulation tasks, ForeTac-VLA achieves an average success rate of 95%, outperforming the fine-tuned VLA model by 36.25 percentage points and state-of-the-art tactile-enhanced VLA baselines by over 22 percentage points. ForeTac-VLA also maintains strong performance under low-illumination and visually cluttered conditions. Video demonstrations can be found on https://foretac-vla.github.io/

