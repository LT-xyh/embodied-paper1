---
type: paper
node_id: paper:fan2025_longvla_unleashing_longhorizon
title: "Long-VLA: Unleashing Long-Horizon Capability of Vision Language Action Model for Robot Manipulation"
authors: ["Yiguo Fan", "Pengxiang Ding", "Shuanghao Bai", "Xinyang Tong", "Yuyang Zhu", "Hongchao Lu", "Fengqi Dai", "Wei Zhao", "Yang Liu", "Siteng Huang", "Zhaoxin Fan", "Badong Chen", "Donglin Wang"]
year: 2025
venue: "arXiv"
external_ids:
  arxiv: "2508.19958"
  doi: null
  s2: null
tags: ["long-horizon", "VLA"]
added: 2026-09-29T01:39:52Z
---

# Long-VLA: Unleashing Long-Horizon Capability of Vision Language Action Model for Robot Manipulation

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

> Vision-Language-Action (VLA) models have become a cornerstone in robotic policy learning, leveraging large-scale multimodal data for robust and scalable control. However, existing VLA frameworks primarily address short-horizon tasks, and their effectiveness on long-horizon, multi-step robotic manipulation remains limited due to challenges in skill chaining and subtask dependencies. In this work, we introduce Long-VLA, the first end-to-end VLA model specifically designed for long-horizon robotic tasks. Our approach features a novel phase-aware input masking strategy that adaptively segments each subtask into moving and interaction phases, enabling the model to focus on phase-relevant sensory cues and enhancing subtask compatibility. This unified strategy preserves the scalability and data efficiency of VLA training, and our architecture-agnostic module can be seamlessly integrated into existing VLA models. We further propose the L-CALVIN benchmark to systematically evaluate long-horizon manipulation. Extensive experiments on both simulated and real-world tasks demonstrate that Long-VLA significantly outperforms prior state-of-the-art methods, establishing a new baseline for long-horizon robotic control.

