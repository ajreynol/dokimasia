#!/usr/bin/env python3
"""Mint an id, or the stable record an independent producer fills with evidence."""
import argparse
from pathlib import Path
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dokimasia_analyzer.findings import finding_id, observation

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("code")
    ap.add_argument("entity")
    ap.add_argument("--record", action="store_true")
    args = ap.parse_args()
    try:
        print(json.dumps(observation(args.code, args.entity), indent=2) if args.record
              else finding_id(args.code, args.entity))
    except ValueError as e:
        ap.error(str(e))
