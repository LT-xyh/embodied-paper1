---
type: paper
node_id: paper:zhang2025_experiences_from_benchmarking
title: "Experiences from Benchmarking Vision-Language-Action Models for Robotic Manipulation"
authors: ["Yihao Zhang", "Yuankai Qi", "Xi Zheng"]
year: 2025
venue: "arXiv"
external_ids:
  arxiv: "2511.11298"
  doi: null
  s2: null
tags: ["evaluation", "benchmark"]
added: 2026-09-29T01:45:50Z
---

# Experiences from Benchmarking Vision-Language-Action Models for Robotic Manipulation

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

> Foundation models applied in robotics, particularly \textbf{Vision--Language--Action (VLA)} models, hold great promise for achieving general-purpose manipulation. Yet, systematic real-world evaluations and cross-model comparisons remain scarce. This paper reports our \textbf{empirical experiences} from benchmarking four representative VLAs -- \textbf{ACT}, \textbf{OpenVLA--OFT}, \textbf{RDT-1B}, and \boldmath{$π_0$} -- across four manipulation tasks conducted in both simulation and on the \textbf{ALOHA Mobile} platform. We establish a \textbf{standardized evaluation framework} that measures performance along three key dimensions: (1) \textit{accuracy and efficiency} (success rate and time-to-success), (2) \textit{adaptability} across in-distribution, spatial out-of-distribution, and instance-plus-spatial out-of-distribution settings, and (3) \textit{language instruction-following accuracy}. Through this process, we observe that \boldmath{$π_0$} demonstrates superior adaptability in out-of-distribution scenarios, while \textbf{ACT} provides the highest stability in-distribution. Further analysis highlights differences in computational demands, data-scaling behavior, and recurring failure modes such as near-miss grasps, premature releases, and long-horizon state drift. These findings reveal practical trade-offs among VLA model architectures in balancing precision, generalization, and deployment cost, offering actionable insights for selecting and deploying VLAs in real-world robotic manipulation tasks.

