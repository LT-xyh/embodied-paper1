#!/usr/bin/env python3
"""Download the predeclared FreeTacMan subset with byte/hash accounting."""
from __future__ import annotations
import hashlib, json, pathlib, urllib.parse, urllib.request

REV = "030316fb41d6fa1e58cccb4bbe0f6fddbb932671"
BASE = f"https://huggingface.co/datasets/OpenDriveLab/FreeTacMan/resolve/{REV}/"
TASKS = ["Stamp", "UsbPlug", "FragileCup"]
ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
TREE_FILES = {"Stamp": "/tmp/Stamp.json", "UsbPlug": "/tmp/UsbPlug.json", "FragileCup": "/tmp/FragileCup.json"}

def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    entries = []
    for task in TASKS:
        listing = json.loads(pathlib.Path(TREE_FILES[task]).read_text())
        for item in listing:
            path = item.get("path", "")
            name = pathlib.Path(path).name.lower()
            if item.get("type") != "file" or not (name.endswith("_camera1.mp4") or name.endswith("_camera2.mp4") or name.endswith("_traj.csv")):
                continue
            entries.append({"path": path, "expected_bytes": item.get("size"), "oid": item.get("oid"), "task": task})
    entries.sort(key=lambda x: x["path"])
    manifest = {"dataset_revision": REV, "tasks": TASKS, "predeclared": True, "files": entries, "expected_total_bytes": sum(x["expected_bytes"] or 0 for x in entries)}
    (ROOT / "subset_manifest.expected.json").write_text(json.dumps(manifest, indent=2) + "\n")
    RAW.mkdir(parents=True, exist_ok=True)
    for item in entries:
        rel = pathlib.Path(item["path"])
        dest = RAW / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.stat().st_size != item["expected_bytes"]:
            url = BASE + urllib.parse.quote(item["path"])
            print(f"GET {item['path']} ({item['expected_bytes']} bytes)", flush=True)
            urllib.request.urlretrieve(url, dest)
        actual = dest.stat().st_size
        if item["expected_bytes"] is not None and actual != item["expected_bytes"]:
            raise RuntimeError(f"size mismatch {dest}: {actual} != {item['expected_bytes']}")
        item["actual_bytes"] = actual
        item["sha256"] = sha256(dest)
    manifest["downloaded_total_bytes"] = sum(x["actual_bytes"] for x in entries)
    manifest["files"] = entries
    (ROOT / "subset_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"files": len(entries), "expected_total_bytes": manifest["expected_total_bytes"], "downloaded_total_bytes": manifest["downloaded_total_bytes"]}, indent=2))

if __name__ == "__main__":
    main()
