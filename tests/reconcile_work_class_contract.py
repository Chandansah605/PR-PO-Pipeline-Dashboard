#!/usr/bin/env python3
"""Fail when the dashboard and email sender work-class contracts drift."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy-repo", required=True)
    args = parser.parse_args()
    dashboard_root = Path(__file__).resolve().parents[1]
    proxy_root = Path(args.proxy_repo).resolve()
    dashboard = json.loads((dashboard_root / "work-class-rule.json").read_text(encoding="utf-8"))
    sender = json.loads((proxy_root / "work-class-rule.json").read_text(encoding="utf-8"))
    if dashboard != sender:
        raise SystemExit("dashboard and email sender work-class contracts have drifted")
    print("Dashboard and email sender work-class contracts match")


if __name__ == "__main__":
    main()
