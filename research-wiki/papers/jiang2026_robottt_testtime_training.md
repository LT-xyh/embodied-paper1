---
type: paper
node_id: paper:jiang2026_robottt_testtime_training
title: "RoboTTT: Test-Time Training for Vision-Language-Action Policies"
authors: ["Yunfan Jiang", "Yevgen Chebotar", "Ruijie Zheng", "Fengyuan Hu", "Yunhao Ge", "Jimmy Wu", "Tianyuan Dai", "Scott Reed", "Li Fei-Fei", "Yuke Zhu", "Linxi \"Jim\" Fan"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2607.15275"
  doi: null
  s2: null
tags: ["inference-time", "adaptation"]
added: 2026-09-29T01:39:46Z
---

# RoboTTT: Test-Time Training for Vision-Language-Action Policies

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

> Recent robot foundation models operate with single-step or short-history visuomotor context. We introduce Test-Time-Training Robot Policies (RoboTTT), a robot model and training recipe that scale visuomotor context to 8K timesteps, three orders of magnitude beyond state-of-the-art policies, without growing inference latency. At this context length, we unlock new robot capabilities: one-shot in-context imitation from human video demonstrations, on-the-fly policy improvement, robustness to perturbations, and stronger performance on multi-stage, long-horizon tasks. We also observe, for the first time, steady gains in closed-loop performance as pretraining context length scales. At its core, RoboTTT integrates Test-Time Training into robot foundation models such as Vision-Language-Action policies, yielding a sequence model whose recurrent state consists of fast weights, parameters updated by gradient descent during both training and inference, compressing histories into weight space and retrieving contextual information for long-context conditioning. To scale training context length, the recipe combines sequence action forcing with truncated backpropagation through time. On challenging real-robot manipulation tasks, RoboTTT improves overall performance by 87% over the single-step context baseline and fully completes a five-minute, ten-stage assembly task, which no baseline ever does. RoboTTT trained with 8K-timestep context outperforms the same model pretrained with 1K timesteps by 62%, suggesting context length as a new scaling axis for robot foundation models. Videos are available at https://research.nvidia.com/labs/gear/robottt/

