"""Standalone proofless preprocessing lemma report."""
import argparse
import json

from .scan import scan


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=['check'])
    ap.add_argument('cvc5')
    args = ap.parse_args(argv)
    r = scan(args.cvc5)
    print(f'{r.methods} output methods; {r.reachable} local ppRewrite paths; '
          f'{r.guarded} paths with proof handling left unknown')
    for issue in r.issues:
        print(json.dumps(issue, sort_keys=True))
    print(f'{len(r.issues)} explicit null-generator lemma sites (final-proof reachability untested)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
