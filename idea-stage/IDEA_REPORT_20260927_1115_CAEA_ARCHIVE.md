# New Embodied AI Research-Direction Discovery — 2026-09-27

## Scope and governance

This is a new discovery cycle. The abandoned Action-Swap Consequence Consistency (ASCC) pilot is treated as negative evidence, not as a seed for repair or renamed variants. The validated native MuJoCo intervention substrate and robosuite wrapper-closure qualification are reusable infrastructure only. No method implementation, training, simulator rollout, VLA inference, or scientific pilot was run in this cycle.

The search targets a focused Paper-1 contribution in embodied AI / robot learning with a falsifiable 1–3 day pilot, moderate compute, and a path to a multi-task evaluation. Generic memory auxiliaries, transition-surprise memory, ordinary predictive losses, generic counterfactual consistency, world-model evaluator diagnosis, benchmark-only audits, and action-swap auxiliary-loss variants are excluded.

## Literature landscape

Recent work makes a generic “counterfactual robot policy evaluation” claim unsafe. Counterfactual Memory Audit (CMA, arXiv:2609.27247, Sep. 2026) explicitly crosses histories at verified-identical present states and separates memory sensitivity, warranted choice, matched-world value, and reliability: https://arxiv.org/abs/2609.27247. WorldEcho/WorldSync (arXiv:2608.24885) already studies off-expert action following and intervention-effect alignment for action-conditioned world models: https://arxiv.org/abs/2608.24885. PACT (arXiv:2606.03949) uses counterfactual advantage for human-in-the-loop credit correction, so a generic counterfactual advantage signal is also crowded. Action-Free Reasoning for Policy Generalization (CoRL 2025) demonstrates that non-action information can change robot-policy generalization, while Redundancy-aware Action Spaces (2024) directly studies action redundancy and task/joint-space tradeoffs. Standard policy-evaluation infrastructure such as SIMPLER (CoRL 2025) and broad VLA evaluation protocols further reduce the novelty of a metric-only benchmark.

The landscape leaves a narrower opening: use *physical successor effects of executable actions* to audit the causal geometry of a frozen policy's local decision, while explicitly excluding history-memory auditing, learned-world-model alignment, confidence calibration alone, and a training loss. The scientific object is a policy–environment relation measured at cloned states, not a new recurrent architecture.

## Ranked ideas

The ranked set contains one cautious survivor and two rejected comparators after aggressive novelty screening.

### 1. Causal Action-Effect Alignment (CAEA)

**Failure mode.** A policy can select a low-loss or familiar action whose local physical consequence is poor, especially near contact and branching states. Standard BC success conflates policy choice with environment sensitivity.

**Hypothesis.** At a cloned state, the policy's local action ranking (or action margin) predicts which executable perturbation has the best short-horizon task consequence only when the policy has learned a causally meaningful decision boundary. The alignment should be stronger for successful policies and should predict imminent failure before a success metric changes.

**Robot-specific adaptation.** Construct a small, bounded action neighborhood around the policy action; execute each candidate from the identical wrapper-level state in fresh subprocesses; score short-horizon successor progress and contact/task validity. Compare the policy's action score/margin to the measured consequence ranking. This is an intervention on the real simulator transition, not a learned world model, not a memory-history swap, and not an auxiliary training loss.

**Closest prior and boundary.** CMA audits whether history changes alter actions and whether those changes are warranted; CAEA holds history fixed and asks whether *the action currently preferred by the policy* is physically better than nearby valid alternatives. WorldSync aligns learned world-model intervention effects, not a frozen policy's local action ranking against ground-truth successor outcomes. PACT uses counterfactual advantage to train human-feedback credit, not a diagnostic of BC action-effect alignment. “When to Act” (arXiv:2601.04982) calibrates confidence for human-intention prediction, not action consequence. The claim must not be phrased as generic counterfactual policy evaluation.

**Minimum discriminating pilot (not executed).** State-only BC-RNN on Lift and Can; sample 30–50 cloned states per task from held-out demonstrations and policy rollouts. For each state, evaluate the policy action plus 4–8 bounded action perturbations for 5–10 simulator steps. Compute Kendall/Spearman rank correlation between policy action likelihood/margin and measured progress, top-1 causal regret, and failure-onset lead time. Controls: random action ranking, nearest-demonstration action ranking, next-state-prediction ranking, and equal-distance perturbations. Use fresh processes and the already-qualified wrapper closure.

**Positive / null / negative.** Positive: alignment above all controls and predicts failure onset across Lift and Can with held-out states. Null: no alignment but task success unchanged, implying policy scores are not locally causal. Negative: alignment appears only in one task or is explained by action distance/contact heuristics; reject the scientific claim.

**Compute and scope.** CPU MuJoCo, 2 tasks, 3 seeds, roughly 1–3 days including instrumentation; no VLA training. Existing native and wrapper intervention infrastructure is sufficient. Main risk is metric-only contribution; the paper must center a falsifiable causal finding and an actionable failure decomposition, not propose a new score alone.

### 2. Action-Equivalence and Policy Arbitrariness Audit (AEPAA)

**Failure mode.** Redundant continuous actions can be physically interchangeable over a short horizon, yet a policy may oscillate or make arbitrary choices across equivalent action classes, causing brittle contact behavior and poor reproducibility.

**Hypothesis.** The size and geometry of local action-equivalence classes (actions with statistically indistinguishable short-horizon successors) predicts policy instability and failure more reliably than Euclidean action variance. Policies trained with identical demonstrations can differ mainly in how they resolve physically equivalent actions.

**Robot-specific adaptation.** Infer equivalence classes from real same-state simulator successors under bounded action perturbations, including contact/task outputs. Measure policy consistency across cloned states and seeds, then relate class-boundary crossings to failure. This tests physical action redundancy rather than changing the action space or adding a loss.

**Closest prior and boundary.** Redundancy-aware Action Spaces studies action-space design and representation efficiency, not a frozen-policy audit of local physical equivalence classes. CMA studies history-conditioned action changes, not action interchangeability at fixed history. WorldSync is a learned world-model alignment method. The direct-prior risk is high: if the result reduces to a new action-space metric or generic robustness benchmark, reject.

**Minimum discriminating pilot (not executed).** Lift/Can, 30 cloned states per task, 16 bounded actions per state, 5-step successors. Cluster successors using task-relevant state/contact features with preregistered tolerances. Compare policy action choice entropy within an equivalence class, class-crossing rate, and downstream failure against Euclidean action variance and random policy controls.

**Positive / null / negative.** Positive: equivalence-aware instability predicts failures across tasks/seeds and survives action-distance controls. Null: equivalence classes add no predictive value beyond distance. Negative: classes are task-specific or tolerance-dependent; reject.

**Compute and scope.** CPU-only, likely 1–3 days; no new runtime. Main risk is direct collision with action-space redundancy literature and benchmark-only framing, so admission requires a mechanism claim about physical equivalence-induced policy arbitrariness.

### 3. Causal Decision-Boundary Stress Test (CDBST) — provisional reject

This probes whether small state-preserving or physically irrelevant perturbations flip policy actions near true consequence boundaries. It is easy to run with cloned states, but CMA and broad behavioral/representational diagnostic work already cover history sensitivity and action reliability. Without a new intervention variable or mechanistic training consequence, this is a generic robustness metric. It is retained only as a rejected comparator, not a Paper-1 candidate.

## Novelty verification

| Candidate | Direct collisions checked | Non-overlapping claim | Status |
|---|---|---|---|
| CAEA | CMA; WorldEcho/WorldSync; PACT; confidence calibration; generic VLA evaluation | Fixed-history policy-score ranking versus ground-truth local physical action consequences, with failure-onset prediction | **Survivor with caution** |
| AEPAA | Redundancy-aware Action Spaces; CMA; generic robustness/evaluation | Physical successor-equivalence classes explain policy arbitrariness and instability at fixed state | **Rejected after review** |
| CDBST | CMA and behavioral diagnostic literature | None strong enough beyond a metric/benchmark change | **Rejected** |

The novelty claim is intentionally narrow. Neither CAEA nor AEPAA is authorized for implementation from this report; the report only defines the minimum discriminating experiments and rejection criteria.

## External critical review

Independent review receipt: `gpt-6-astra / medium`, thread `/root/new_direction_reviewer`, trace `.aris/traces/idea-discovery/2026-09-27_run01/002-independent-review-new-direction`.

The reviewer verdict is **CAEA — PROCEED WITH CAUTION** and **AEPAA — ABANDON**. CAEA is substantively distinct only when the claim is fixed-state/fixed-history policy preference versus ground-truth simulator successor value. The strongest objection is score identifiability: continuous BC-RNN may not expose a calibrated score over candidate actions, allowing action-distance or contact heuristics to explain the result. The required gate is therefore an explicit candidate-score identifiability test, equal-radius balanced perturbations, exact cloned-state fresh-process execution, and preregistered controls for random ranking, nearest-demo/distance, next-state prediction, transition surprise, contrastive/action-conditioned representations, adaptive memory, and CMA history swaps. AEPAA is abandoned because physical equivalence classes are researcher-defined and collapse toward action-space redundancy, action variance, or generic robustness evaluation. CDBST remains abandoned as generic perturbation robustness.

## Candidate comparison and recommendation

CAEA is the sole surviving direction, with a cautionary admission. AEPAA and CDBST are rejected. No pilot is executed in this discovery cycle. If the score-identifiability gate passes later, the first pilot is CAEA on state-only BC-RNN Lift/Can with fresh-process cloned-state interventions and preregistered controls; otherwise the direction is abandoned without tuning or renaming.

<!-- ARIS_IDEA_DISCOVERY_EVIDENCE_GATE:START -->
## Evidence Gate
**Status:** PASS

All required stage records, review receipts, artifacts, and report sections are present.
<!-- ARIS_IDEA_DISCOVERY_EVIDENCE_GATE:END -->
