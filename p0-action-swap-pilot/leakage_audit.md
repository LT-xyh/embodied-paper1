# ASCC Pilot Leakage Audit

- Each class state was made from a captured complete wrapper snapshot and altered only in the hidden cube free-joint x coordinate (native state qpos index 10; state vector index includes leading time).
- Factual and alternate consequences were produced by independently restoring the same serialized state and calling `env.step` with `[+1,0,0,0,0,0,-1]` and `[-1,0,0,0,0,0,-1]`.
- Provenance hashes are recorded for every pair in `action_swap_pilot_results.json`; no cross-trajectory action or successor was copied.
- Policy observations contain only robot joint/gripper state. Cube pose, object-state, trajectory id, episode id, phase, intervention id, reward and target metadata are excluded.
- History cue is a real robot-joint state observation from a separately restored valid state; the final alias observation is shared robot state while cube latent x differs.
- The negative control shuffles ASCC labels within the training split while preserving capacity, data count, and loss scale.
- No normalization, frame stack, or hidden preprocessing cache exists in this direct state-only path.

Limitation: the pilot has only two latent classes and repeated copies per class. The result is a bounded falsification pilot, not a full dataset or benchmark claim.
