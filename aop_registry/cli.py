"""Command line interface for the registry.

    publish   Publish an AOP document (immutable, versioned).
    resolve   Resolve a ref to its catalogue entry.
    verify    Walk the provenance chain for a published ref.
"""

from __future__ import annotations

import argparse
import json
import sys

from .catalogue import Registry


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aop_registry", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("publish")
    p.add_argument("aop")
    p.add_argument("--root", required=True)
    p = sub.add_parser("resolve")
    p.add_argument("ref")
    p.add_argument("--root", required=True)
    p = sub.add_parser("verify")
    p.add_argument("ref")
    p.add_argument("--root", required=True)
    p.add_argument("--cases", required=True)

    args = parser.parse_args(argv)
    registry = Registry(args.root)

    if args.command == "publish":
        entry = registry.publish(args.aop)
        print(json.dumps(entry, indent=2))
        return 0
    if args.command == "resolve":
        entry = registry.resolve(args.ref)
        print(json.dumps(entry, indent=2) if entry else "not found: %s" % args.ref)
        return 0 if entry else 1
    if args.command == "verify":
        result = registry.provenance_chain(args.ref, args.cases)
        print(json.dumps(result, indent=2))
        return 0 if result["holds"] else 1


if __name__ == "__main__":
    sys.exit(main())
