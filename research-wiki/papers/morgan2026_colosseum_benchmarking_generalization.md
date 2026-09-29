---
type: paper
node_id: paper:morgan2026_colosseum_benchmarking_generalization
title: "Colosseum V2: Benchmarking Generalization for Vision Language Action Models"
authors: ["Jeremy Morgan", "Hyeonho Oh", "Prajwal Vijay", "Jincen Song", "Ashvin Arora", "Hojung Lim", "Alina Du", "Jesse Thomason", "Gaurav Sukhatme", "Ishika Singh"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2605.27759"
  doi: null
  s2: null
tags: ["generalization", "benchmark", "OOD"]
added: 2026-09-29T01:45:46Z
---

# Colosseum V2: Benchmarking Generalization for Vision Language Action Models

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

> Vision-Language-Action (VLA) models demonstrate promising generalization in robotic manipulation, driven by advances in large-scale vision and language pre-training. This progress can be misleading. Despite the zero-shot perception and language capabilities of VLAs, their overall task performance often degrades under distribution shifts, revealing gaps in how these systems translate high-level understanding into robust behavior. To systematically study this gap, we introduce Colosseum V2, a large-scale simulation benchmark for evaluating VLA generalization in robot learning across diverse conditions. The benchmark comprises 28 tasks spanning 13 task categories and two robot morphologies, covering a wide range of manipulation primitives and long-horizon behaviors. Built on the ManiSkill simulator, Colosseum V2 enables fast, GPU-parallelized evaluation and supports both in-domain and out-of-domain testing at scale. We evaluate state-of-the-art methods, including Action Chunking Transformers (ACT) and Pi0.5, and reveal limitations in both base performance and generalization. We demonstrate strong correlations between simulation and real-world metrics that support the ecological validity of the benchmark. By standardizing tasks, metrics, and evaluation protocols within a unified benchmark, Colosseum V2 enables reproducible and fair comparisons, reduced evaluation overhead, and accelerated progress toward general-purpose robot policies.

