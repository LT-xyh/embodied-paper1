---
type: paper
node_id: paper:he2026_rct_robotcollected_touchvisionlanguage
title: "RCT: A Robot-Collected Touch–Vision–Language Dataset for Tactile Generalization"
authors: ["Jingbo He", "Michael Färber", "Roberto Calandra"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2606.31694"
  doi: null
  s2: null
tags: ["tactile", "multimodal", "dataset"]
added: 2026-09-29T01:39:47Z
---

# RCT: A Robot-Collected Touch–Vision–Language Dataset for Tactile Generalization

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

> For robots manipulating open-world objects, tactile representations must generalize to unseen materials. We introduce RCT (Robotic Contact Tactile), a robot-collected touch-vision-language dataset with 29,279 tactile frames from full robot presses on 122 industrial reference materials in 7 categories, recorded with three DIGIT sensors at multiple contact positions. RCT preserves each press as a contact sequence, enabling held-out evaluation across materials, categories, sensors, contact positions, and contact sequences. Frames from one press are strongly correlated: frame-random splits can place near-duplicate observations of the same physical interaction in both training and test. With the encoder held fixed, removing contact-sequence overlap reduces tactile-to-text Recall@1 by 17.7 percentage points. When materials are additionally held out at training time, performance drops sharply, leaving held-out-material Recall@1 at 25.1 +/- 6.1% averaged over three held-out draws. The public TVL/HCT split shows the same structure: every test contact sequence appears in training, and raw-pixel nearest neighbors recover the correct sequence in 98.3% of cases. Uniformly sampling a press improves contrastive training, and RCT-trained embeddings improve category probes on unseen materials. RCT makes contact-sequence-aware, held-out-material evaluation reproducible and exposes novel-material generalization as a central challenge for robotic tactile perception. The RCT dataset is open-sourced at https://faerber-lab.github.io/RCT/

