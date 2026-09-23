#!/usr/bin/env python3
"""Validate the bounded P0 stop record; no scientific metrics were produced."""
import json
from pathlib import Path

RESULTS = Path(__file__).with_name("results.json")


def main() -> None:
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    assert data["verdict"] == "PIVOT — RUNTIME"
    assert data["runtime"]["gate"] == "FAIL"
    assert data["experiment"]["p0_a"].startswith("NOT ENTERED")
    assert data["experiment"]["p0_b"] == "NOT ENTERED"
    assert data["experiment"]["rollouts"] == 0
    assert data["experiment"]["policy_seeds_trained"] == []
    assert data["downloads"]["dataset_checkpoint_video_bytes"] == 0
    print("Stop record is internally consistent; no scientific result table exists.")


if __name__ == "__main__":
    main()
