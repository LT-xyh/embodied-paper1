# TCI horizon specification

For each cloned state and each of five candidates, the branch is restored in a fresh subprocess, the candidate is stepped once, and the same deterministic controller is stepped for the remaining horizon. Horizons are H=1, 4, and 12 simulator steps. The consequence vector records task-relevant state quantities (EEF-to-cube distance, cube z, cumulative reward, done) and uses `G_H = -eef_cube_distance` for the rank/inversion analysis. Inversion is `sign(D_1) != sign(D_12)` with both magnitudes greater than 0.005, where `D_H=G_H(chosen)-G_H(alternative)`.
