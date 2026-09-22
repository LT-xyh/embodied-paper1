# Venue-First Contribution-Bar Recalibration

**Status:** ACTIVE STRATEGY AUTHORITY  
**Date:** 2026-09-22  
**Binding context:** `RESEARCH_BRIEF.md`

## Purpose

Multiple high-bar research-selection passes returned zero candidates:

- substrate-first;
- high-bar substrate-first;
- baseline-first robot-method search;
- adjacent-field method transfer.

Do not start another idea search yet.

The objective is to recalibrate the research admission bar against the user's actual publication target:

> satisfy at least one of:
> - CCF B conference or above;
> - CAS Zone 3 journal or above.

The fastest credible route may therefore be a journal contribution whose novelty is below the bar previously used for conference-style method admission.

## Phase 1 — Target-venue verification

Identify **3-5 realistic journals** that currently satisfy CAS Zone 3 or above and publish work relevant to:

- robot learning;
- robotic manipulation;
- imitation learning;
- embodied intelligence;
- intelligent control;
- autonomous systems;
- learning-based robotics.

Use current publicly verifiable ranking information. Record:

- journal title;
- publisher;
- latest available CAS zone classification and year/source;
- scope fit;
- typical article type;
- publication cadence / review-time evidence where publicly stated;
- open-access or APC considerations if relevant.

Do not assume a journal's current zone from old memory.

If exact CAS zoning cannot be verified from a reliable current public source, mark it **UNVERIFIED** rather than guessing.

## Phase 2 — Recent-paper contribution audit

For each verified or high-confidence target venue, inspect recent 2024-2026 papers relevant to the project.

Sample enough papers to infer the contribution bar, not just one unusually strong article.

For each relevant paper classify the dominant contribution as one or more of:

- genuinely new learning mechanism;
- incremental method extension;
- combination of known methods with a robot-specific formulation;
- systematic empirical study;
- benchmark/evaluation contribution;
- application/system contribution with technical novelty;
- review/survey;
- other.

Record:

- exact paper;
- year;
- problem;
- method delta;
- evaluation breadth;
- whether real robot is required;
- whether the contribution would have passed the current project's previous hard novelty gate.

## Phase 3 — Calibrate two publication bars

Define separately:

### Track A — Fast journal route

The minimum contribution bar that appears credible for a CAS Zone 3-or-above journal under the user's 1-3 month goal.

This bar may allow:

- a technically meaningful incremental method;
- a principled combination of known methods;
- a systematic empirical result with a clear scientific question;
- a lightweight robot-specific adaptation;

provided that:

- it is not a direct reproduction;
- there is a clear problem statement and technical contribution;
- experiments are broad enough for the venue;
- the result is reproducible and not benchmark QA only.

### Track B — Higher-upside conference route

Retain the stronger method novelty bar appropriate for CCF B-or-above conference targeting.

Do not blur the two.

## Phase 4 — Re-evaluate previous near-misses under Track A

Revisit only the strongest previously rejected directions, including:

- robomimic baseline-first near-misses;
- adjacent-field near-misses;
- Armnet only if the venue audit shows benchmark/data-method studies of comparable strength;
- other recorded candidates only if their previous rejection was caused primarily by an overly strong novelty bar rather than a direct prior collision.

Do **not** revive candidates with explicit direct collisions such as:

- GPC-equivalent policy composition;
- Q-Planning-equivalent frozen-BC/Q selection;
- ISR-equivalent trajectory resampling;
- SDP-equivalent correction loss;
- MTIL/Mamba Policy-equivalent SSM policy design;
- conformal robot safety / ConformalDAgger-equivalent uncertainty methods;
- distributionally robust offline imitation learning already covered by direct 2026 prior.

A candidate may be reconsidered only when the remaining delta is genuinely nontrivial and empirically testable.

## Phase 5 — Recommend the next research bar

Return one of:

- **FAST-JOURNAL BAR ADOPTED**
- **CONFERENCE BAR RETAINED**
- **PUBLICATION TARGET MUST CHANGE**

Then specify:

- target venue family;
- minimum acceptable contribution type;
- minimum experiment package;
- whether a 1-2 month first draft is realistic;
- what kinds of ideas should now be admitted or rejected.

This report may recommend a new candidate-search contract, but must not itself run that search.

## Required output

Write:

`idea-stage/VENUE_FIRST_RECALIBRATION_REPORT.md`

Required sections:

1. **Verified Target Venues**
2. **Recent 2024-2026 Paper Sample**
3. **Observed Contribution Patterns**
4. **Fast-Journal Contribution Bar**
5. **CCF-B Conference Contribution Bar**
6. **Previous Near-Miss Reassessment**
7. **Recommended Publication Strategy**
8. **Recommended Next Search Contract**, but do not execute it

Update `MANIFEST.md`, commit, push, and stop.

## Stop rule

Do not:

- generate another broad idea list;
- install runtimes;
- train policies;
- run simulators;
- download large datasets/checkpoints;
- start a P0;
- start `/research-pipeline`.

This is a publication-strategy calibration pass only.
