---
type: paper
node_id: paper:domae2026_embodiment_gap_robot
title: "The Embodiment Gap in Robot Foundation Models"
authors: ["Yukiyasu Domae", "Keisuke Shirai", "Hanbit Oh", "Ryoichi Nakajo", "Tomohiro Motoda", "Koshi Makihara", "Masaki Murooka", "Takuma Yagi", "Yoshiaki Bando", "Ryo Hanai"]
year: 2026
venue: "Transactions on Machine Learning Research, August 2026"
external_ids:
  arxiv: "2608.18433"
  doi: null
  s2: null
tags: ["cross-embodiment", "generalization"]
added: 2026-09-29T01:39:41Z
---

# The Embodiment Gap in Robot Foundation Models

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

> Robot foundation models (RFMs), including vision-language-action (VLA) policies, are often discussed through a scaling view: more data, larger models, and broader benchmarks should improve generalization. In robotics, however, a model can generalize while work still remains before it can run on a robot with a particular body. The work required differs across methods and target robots, and those differences affect practical deployment. We call the gap between reusable models, representations, or data and their use in execution on the target robot the embodiment gap. This survey examines what can be reused across robot embodiments and what must still be implemented on a new robot. We place existing methods on a two-axis map that shows the type of shared structure and the stage at which adaptation is needed for execution on the target robot. We then examine recent work through three overlapping research directions: sharing semantics and perception, sharing robot data and interfaces, and learning correspondence across embodiments. We also propose a reporting framework for adaptation work that success rate alone does not reveal. The framework identifies the work that should be checked when comparing cross-embodiment learning and highlights work that remains on a new robot and questions for future study.

