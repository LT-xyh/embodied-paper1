# Focused Tactile / Physical Grounding Idea Discovery

Date: 2026-09-29  
Scope: FreeTacMan offline behavioral proxy, with RCT as a supporting leakage-controlled tactile benchmark  
Status: **READY FOR MINIMUM SCIENTIFIC PILOT**

No method was implemented and no pilot, training, download, simulator, GPU, or hardware experiment was run.

## Binding substrate constraints

The only currently admitted substrate is a small, preregistered FreeTacMan subset. The first scientific run must freeze the exact Git/Hugging Face revisions, file hashes and byte count; retain complete episodes; split by episode and, where possible, object/task category; audit timestamps, tactile calibration, coordinate conventions, action clipping, and outcome labels. The claim is limited to offline control-relevant generalization. RCT can validate tactile representation and contact-sequence split hygiene, but cannot validate policy behavior because it has no action trajectories.

## Candidate questions

### Candidate 1 — Contact-conditional control value of tactile input (RECOMMENDED)

**Question.** Does tactile input provide incremental action information only during contact transitions, or does it improve control prediction throughout a trajectory?

**Hypothesis.** Under episode/object/task-disjoint evaluation, tactile input yields its largest marginal reduction in multi-step TCP/gripper error during contact-entry, sustained-contact, and release phases, while vision-plus-proprioception remains competitive in free-space motion. The phase pattern should replicate across 3–5 contact-diverse tasks rather than appear as a global average artifact.

**Measurement.** Compare matched RGB+proprio current-frame and short-history BC against RGB+tactile+proprio variants. Report per-phase one-step and multi-step action error, normalized trajectory distance, paired bootstrap intervals, calibration, and the tactile marginal after parameter/history matching. Phase labels must be derived only from released force/tactile/trajectory signals and frozen before testing.

**Closest prior and distinction.** PACE already proposes phase-aware contact-event conditioning for chunk-based insertion policies; TacO and ManiFeel already compare tactile modalities and policy success; FreeTacMan reports tactile-versus-vision policy gains. The non-overlapping claim here is an attribution study: whether the tactile marginal is localized to contact phases under leakage-resistant task/object splits, not a new fusion module, benchmark score, or chunking rule. A null result is informative because it would reject the assumed phase-local mechanism.

**Minimum pilot.** Three seeds, 3–5 tasks, 100–300 complete trajectories if available, no frame-random split, four matched controls (RGB current, RGB history, tactile+RGB current, tactile+RGB history), and phase-stratified metrics.

**Kill rule.** Kill if the tactile gain disappears under episode/object-disjoint splits, appears only in one task, is explained by history or parameter count, or cannot be assigned reliable contact phases.

**Resource cost.** Low to moderate CPU/GPU training on a small subset; no robot, custom sensor, simulator, or large VLA checkpoint.

### Candidate 2 — Sensor- and task-disjoint tactile action transfer (BACKUP)

**Question.** Do tactile features that transfer across sensor instances or materials also transfer to action prediction on unseen tasks or object families?

**Hypothesis.** Representation-level transfer measured on RCT does not guarantee action-level transfer in FreeTacMan; a measurable gap will appear when contact appearance, task, and object identity are held out independently.

**Measurement.** Freeze an encoder or use a matched small encoder, train the same action head on seen conditions, and evaluate action/trajectory error on held-out task/object families and any available sensor split. Report representation retrieval beside action metrics without treating retrieval as behavior.

**Closest prior and distinction.** RCT establishes held-out-material/sensor tactile retrieval; FreeTacMan establishes visuo-tactile imitation and policy gains; TacO and ManiFeel benchmark sensor/policy comparisons. The non-overlapping claim is a cross-level transfer audit linking representation generalization to control prediction, not a new encoder or sensor benchmark.

**Minimum pilot.** One fixed encoder, two or more disjoint task/object splits, three seeds, action and retrieval metrics.

**Kill rule.** Kill if metadata cannot provide disjoint sensor/object/task factors, or if the result reduces to a benchmark re-ranking with no interpretable representation-to-action gap.

**Resource cost.** Moderate metadata and preprocessing burden; higher risk than Candidate 1.

## Rejected directions

- Generic tactile-token or cross-attention fusion: direct and repeated prior in HapTile, Tactile-VLA, ForceVLA, and related systems.
- Future tactile forecasting as the main novelty: direct collision with ForeTac-VLA, TouchWorld, TACO, TTP, and DexTouch-WM.
- Phase-aware gating, contact-event correction, or chunk conditioning: direct collision with PACE and reactive tactile policies.
- A new tactile sensor or custom hardware: violates the access contract.
- RCT-only material classification/retrieval: perception-only and fails the behavioral gate.
- A benchmark-only leaderboard or generic uncertainty/calibration score: insufficient scientific mechanism for this project.

## Recommendation

Authorize exactly one minimum pilot: **Candidate 1, Contact-conditional control value of tactile input**. The pilot is an offline measurement study, not an automatic launch in this session. It must stop and record `PIVOT — ACCESS` if the selected files, action alignment, or leakage-resistant split cannot be verified. It must record a null rather than introduce a new method if the tactile marginal is absent.

The project is therefore **READY FOR MINIMUM SCIENTIFIC PILOT**, with the claim frozen to contact-phase-specific offline action generalization. No full VLA training or real-world claim is authorized.

## Prior evidence

- [RCT](https://faerber-lab.github.io/RCT/)
- [FreeTacMan project](https://opendrivelab.com/FreeTacMan)
- [FreeTacMan code](https://github.com/OpenDriveLab/FreeTacMan)
- [PACE](https://pace-insertion.github.io/)
- [TacO](https://tacobench.github.io/)
- [ManiFeel](https://arxiv.org/abs/2505.18472)
- [ForeTac-VLA](https://arxiv.org/abs/2609.20980)
