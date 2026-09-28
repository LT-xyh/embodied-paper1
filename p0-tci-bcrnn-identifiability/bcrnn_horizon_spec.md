# Policy-faithful horizon specification

For each cloned state and each candidate, the wrapper-level state is restored
in a fresh subprocess. The candidate action is executed first. At subsequent
steps, the same frozen BC-RNN is queried on the new observation with the
branch's recurrent state, so H=4 and H=12 are genuine policy continuations,
not the scripted measurement stub used by the earlier gate. Consequences are
recorded at H in `{1, 4, 12}` using the pre-registered task progress functional
`G_H = -distance(eef,cube) + 4*(cube_z-cube_z_at_capture) + 0.1*cumulative_reward`.

TCI inversion is defined without change as a sign change between
`D_1=G_1(chosen)-G_1(alternative)` and `D_12`, with both magnitudes above
`0.005`. Immediate and rank-aggregated multi-horizon top-1, genuine versus
within-state shuffled consequences, and inversion prevalence are all reported.
