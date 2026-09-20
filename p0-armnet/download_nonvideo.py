#!/usr/bin/env python3
"""Download only the non-video ArmnetBench files used by the bounded P0.

The script refuses video paths, checks the Hugging Face API byte sizes, and
writes a SHA-256 manifest next to the temporary data root. It is deliberately
separate from analysis.py so the analysis can be rerun on an existing cache.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import requests


def list_files(repo: str, revision: str) -> list[dict]:
    url = f"https://huggingface.co/api/datasets/{repo}/tree/{revision}"
    params: dict[str, str] | None = {"recursive": "true", "expand": "true", "limit": "100"}
    entries: list[dict] = []
    while True:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        entries.extend(response.json())
        next_url = response.links.get("next", {}).get("url")
        if not next_url:
            return entries
        url, params = next_url, None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--repo", default="armnet/armnetbench_v01_lerobot_so101")
    parser.add_argument("--revision", default="main")
    args = parser.parse_args()
    if args.root.exists():
        if any(args.root.iterdir()):
            raise RuntimeError(f"refusing non-empty data root: {args.root}")
    else:
        args.root.mkdir(parents=True)
    entries = list_files(args.repo, args.revision)
    files = [
        e for e in entries
        if e.get("type") == "file" and (e["path"].startswith("data/") or e["path"].startswith("meta/"))
    ]
    if any(e["path"].startswith("videos/") for e in files):
        raise RuntimeError("refusing a video path")
    expected = sum(int(e.get("size") or 0) for e in files)
    downloaded = 0
    manifest = []
    for entry in sorted(files, key=lambda e: e["path"]):
        path = entry["path"]
        target = args.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://huggingface.co/datasets/{args.repo}/resolve/{args.revision}/{path}?download=true"
        digest = hashlib.sha256()
        count = 0
        with requests.get(url, stream=True, timeout=120, allow_redirects=True) as response:
            response.raise_for_status()
            with target.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
                        digest.update(chunk)
                        count += len(chunk)
        if count != int(entry.get("size") or 0):
            raise RuntimeError(f"{path}: downloaded {count}, expected {entry.get('size')}")
        downloaded += count
        manifest.append({"path": path, "bytes": count, "sha256": digest.hexdigest(), "oid": entry.get("oid")})
    if downloaded != expected:
        raise RuntimeError(f"downloaded {downloaded}, expected {expected}")
    (args.root / "DOWNLOAD_MANIFEST.json").write_text(
        json.dumps({"repo": args.repo, "revision": args.revision, "expected_bytes": expected, "downloaded_bytes": downloaded, "files": manifest}, indent=2) + "\n"
    )
    print(json.dumps({"repo": args.repo, "revision": args.revision, "files": len(files), "downloaded_bytes": downloaded}, indent=2))


if __name__ == "__main__":
    main()
