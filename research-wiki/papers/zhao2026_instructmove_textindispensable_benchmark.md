---
type: paper
node_id: paper:zhao2026_instructmove_textindispensable_benchmark
title: "InstructMove: A Text-Indispensable Benchmark for Instruction-Following Manipulation"
authors: ["Mengao Zhao", "Ziang Li", "Chaodong Huang", "Mengchen Ma", "Haoyi Jiang", "Yiwei Jin", "Xinjie Wang", "Yun Du", "Xuewu Lin", "Taojun Ding", "Hongyu Xie", "Jackson Jiang", "Chunlei Yu", "Kaihua Zhang", "Lichao Huang", "Liu Liu", "Tianwei Lin", "Zhizhong Su"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2608.22990"
  doi: null
  s2: null
tags: ["language-grounding", "benchmark"]
added: 2026-09-29T01:45:47Z
---

# InstructMove: A Text-Indispensable Benchmark for Instruction-Following Manipulation

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

> Vision-language-action (VLA) models have made general-purpose robot manipulation increasingly plausible by conditioning robot actions on natural-language instructions. A key test of such generality is whether policies actually follow language instructions. Yet many manipulation benchmarks leave this ability underdetermined: the intended object or destination is often visually salient or uniquely feasible, allowing policies to succeed without grounding the instruction. We argue that instruction-following evaluation should be text-indispensable: multiple actions should be visually and physically plausible, while only one should be consistent with the language instruction. We introduce InstructMove, a text-indispensable benchmark for instruction-following manipulation. InstructMove instantiates this principle in pick-and-place scenes with semantic distractors, decomposing instruction following into category identification, attribute discrimination, spatial reasoning, and compositional pick-and-place. InstructMove supports a train-eval protocol with InstructMove training data and held-out evaluation tasks, with additional diagnostics for language dependence. Experiments with representative VLA policies show that InstructMove provides a controlled testbed for diagnosing visual shortcuts and that InstructMove simulation data can improve real-world instruction-following manipulation performance. Code: https://github.com/HorizonRobotics/RoboOrchardSim

