---
type: paper
node_id: paper:quevedo2025_worldgym_world_model
title: "WorldGym: World Model as a Gym for Vision-Language-Action Models"
authors: ["Julian Quevedo", "Ansh Kumar Sharma", "Yixiang Sun", "Varad Suryavanshi", "Percy Liang", "Sherry Yang"]
year: 2025
venue: "arXiv"
external_ids:
  arxiv: "2506.00613"
  doi: null
  s2: null
tags: ["world-model", "evaluation"]
added: 2026-09-29T01:39:53Z
---

# WorldGym: World Model as a Gym for Vision-Language-Action Models

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

> Evaluating robot control policies is difficult: real-world testing is costly, and handcrafted simulators require manual effort to improve in realism and generality. We propose a world-model-based policy evaluation environment (WorldGym), an autoregressive, action-conditioned video generation model which serves as a proxy to real world environments. Policies are evaluated via Monte Carlo rollouts in the world model, with a vision-language model providing rewards. We evaluate a set of VLA-based real-robot policies in the world model using only initial frames from real robots, and show that policy success rates within the world model highly correlate with real-world success rates. Moreoever, we show that WorldGym is able to preserve relative policy rankings across different policy versions, sizes, and training checkpoints. Due to requiring only a single start frame as input, the world model further enables efficient evaluation of robot policies' generalization ability on novel tasks and environments. We find that modern VLA-based robot policies still struggle to distinguish object shapes and can become distracted by adversarial facades of objects. While generating highly realistic object interaction remains challenging, WorldGym faithfully emulates robot motions and offers a practical starting point for safe and reproducible policy evaluation before deployment.

