<!-- ARIS-CODEX:BEGIN -->
## ARIS Codex Skill Scope
ARIS Codex packages installed in this project: skills-codex
Managed entries: 21
Manifest: `.aris/installed-skills-codex.txt`
ARIS repo root: `/public/home/xuyinghao/aris_repo`
Project skill path: `.agents/skills/<skill-name>`
For ARIS Codex workflows, prefer the project-local skills under `.agents/skills/`.
When a skill needs ARIS helper scripts, resolve the repo root from the manifest or set it explicitly:
`ARIS_REPO=$(awk -F'	' '$1=="repo_root"{print $2; exit}' "/public/home/xuyinghao/workspace/embodied-paper1/.aris/installed-skills-codex.txt")`
Do not edit or delete symlinked skills in place; update upstream or rerun:
`bash /public/home/xuyinghao/aris_repo/tools/install_aris_codex.sh "/public/home/xuyinghao/workspace/embodied-paper1" --reconcile`
For copied Codex installs, use:
`bash /public/home/xuyinghao/aris_repo/tools/smart_update_codex.sh --project "/public/home/xuyinghao/workspace/embodied-paper1"`
<!-- ARIS-CODEX:END -->

## Paper-1 Research Governance

The primary objective is the fastest credible scientific path to a publishable Embodied AI / Robot Learning paper, not preservation of previous engineering work.

- Treat `RESEARCH_BRIEF.md` as the binding research-direction contract.
- Ignore sunk engineering cost when selecting or terminating a direction.
- VLA is preferred but not mandatory.
- Prefer simulation-first or offline-data-first validation.
- Define a minimal falsifiable pilot before substantial implementation.
- Prefer core hypotheses that can be supported or killed within 1-3 days.
- Do not serially repair unrelated simulator, runtime, renderer, dependency, or provenance infrastructure before obtaining scientific evidence.
- Infrastructure failure is not scientific evidence.
- Do not launch real-robot experiments without explicit human authorization.
- Do not launch full experiment suites during idea discovery.
- During the first direction-selection phase, stop after the Top-3 candidates.