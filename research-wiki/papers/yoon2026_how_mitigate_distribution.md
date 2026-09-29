---
type: paper
node_id: paper:yoon2026_how_mitigate_distribution
title: "How to Mitigate the Distribution Shift Problem in Robotics Control"
authors: ["Hyung-Suk Yoon", "Seung-Woo Seo"]
year: 2026
venue: "arXiv"
external_ids:
  arxiv: "2605.25414"
  doi: null
  s2: null
tags: ["distribution-shift", "imitation"]
added: 2026-09-29T01:45:49Z
---

# How to Mitigate the Distribution Shift Problem in Robotics Control

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

> Distribution shift in imitation learning refers to the problem that the agent cannot plan proper actions for a state that has not been visited during the training. This problem can be largely attributed to the inherently narrow state-action coverage provided by expert demonstrations over the full environment. In this paper, we propose a robust offline to adaptive online imitation learning framework that handles the distribution shift problem in a lifelong, multi-phase scheme. In the offline learning phase, we leverage supplementary demonstrations to broaden the state-action coverage of the policy by utilizing a discriminator to effectively train the policy with supplementary demonstrations, thereby enhancing the robustness of the policy to distribution shift. In the subsequent online inference phase, our framework detects the occurrence of distribution shift and conducts self-supervised imitation learning from online experiences to adapt the policy to the online environments. Through extensive evaluations in MuJoCo environments, we demonstrate that our method exhibits better robustness to distribution shift and better adaptation performance to online environments than the baseline algorithms, which indicates superior performance of our framework against the distribution shift.

