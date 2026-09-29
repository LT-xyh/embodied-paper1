---
type: paper
node_id: paper:jin2026_beyond_dense_futures
title: "Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation"
authors: ["Minghao Jin", "Mozheng Liao", "Mingfei Han", "Zhihui Li", "Xiaojun Chang"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2603.12553"
  doi: null
  s2: null
tags: ["world-model", "long-horizon"]
added: 2026-09-29T01:45:51Z
---

# Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation

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

> Recent world-model-based Vision-Language-Action (VLA) architectures have improved robotic manipulation through predictive visual foresight. However, dense future prediction introduces visual redundancy and accumulates errors, causing long-horizon plan drift. Meanwhile, recent sparse methods typically represent visual foresight using high-level semantic subtasks or implicit latent states. These representations often lack explicit kinematic grounding, weakening the alignment between planning and low-level execution. To address this, we propose StructVLA, which reformulates a generative world model into an explicit structured planner for reliable control. Instead of dense rollouts or semantic goals, StructVLA predicts sparse, physically meaningful structured frames. Derived from intrinsic kinematic cues (e.g., gripper transitions and kinematic turning points), these frames capture spatiotemporal milestones closely aligned with task progress. We implement this approach through a two-stage training paradigm with a unified discrete token vocabulary: the world model is first trained to predict structured frames and subsequently optimized to map the structured foresight into low-level actions. This approach provides clear physical guidance and bridges visual planning and motion control. In our experiments, StructVLA achieves strong average success rates of 75.0% on SimplerEnv-WidowX and 94.8% on LIBERO. Real-world deployments further demonstrate reliable task completion and robust generalization across both basic pick-and-place and complex long-horizon tasks.

