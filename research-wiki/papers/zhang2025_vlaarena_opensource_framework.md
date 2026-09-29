---
type: paper
node_id: paper:zhang2025_vlaarena_opensource_framework
title: "VLA-Arena: An Open-Source Framework for Benchmarking Vision-Language-Action Models"
authors: ["Borong Zhang", "Jiahao Li", "Jiachen Shen", "Yuhao Zhang", "Yishuai Cai", "Lu Liu", "Hailu Ji", "Yuanpei Chen", "Juntao Dai", "Jiaming Ji", "Yaodong Yang"]
year: 2025
venue: "arXiv"
external_ids:
  arxiv: "2512.22539"
  doi: null
  s2: null
tags: ["evaluation", "benchmark", "language", "robustness"]
added: 2026-09-29T01:45:44Z
---

# VLA-Arena: An Open-Source Framework for Benchmarking Vision-Language-Action Models

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

> While Vision-Language-Action models (VLAs) are rapidly advancing toward generalist robot policies, quantitatively characterizing their capability boundaries and failure modes remains challenging. To address this, we introduce VLA-Arena, a comprehensive benchmark. It features a novel structured task design framework to quantify difficulty across three orthogonal axes: (1) Task Structure, (2) Language Command, and (3) Visual Observation. This allows us to systematically design tasks with fine-grained difficulty levels, enabling a precise measurement of model capability frontiers. For task structure, VLA-Arena comprises 11 task suites organized into four dimensions: Safety, Distractor, Extrapolation, and Long Horizon, totaling 170 tasks. Each suite spans three difficulty levels (L0-L2), with fine-tuning restricted to L0 to rigorously assess generalization. Orthogonal to this, language (W0-W4) and visual (V0-V4) perturbations can be applied to any task as diagnostic probes to distinguish robust grounding from superficial pattern matching. Our extensive evaluation of state-of-the-art VLAs reveals critical limitations: memorization over generalization, superficial visual perception, and a neglect of safety constraints. Additionally, model rank reversals across L0-L2 validate that each level provides non-redundant insights. To foster research addressing these model limitations and ensure reproducibility, we provide the complete VLA-Arena framework, including an end-to-end toolchain from task definition to automated evaluation and the VLA-Arena-S/M/L datasets for fine-tuning. Our benchmark, datasets, models, and leaderboard are publicly available at https://vla-arena.github.io.

