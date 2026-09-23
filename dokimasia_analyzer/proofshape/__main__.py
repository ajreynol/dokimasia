"""Standalone proof construction contract report."""
import argparse
import json

from .scan import scan


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=['check'])
    ap.add_argument('cvc5')
    args = ap.parse_args(argv)
    r = scan(args.cvc5)
    print(f'{r.calls} literal-rule calls; {r.compared} compared on at least one list; '
          f'{r.unknown} unknown; {len(r.ambiguous_rules)} ambiguous rules')
    for issue in r.issues:
        print(json.dumps(issue, sort_keys=True))
    print(f'{len(r.issues)} arity disagreements (syntactic candidates; reachability untested)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
