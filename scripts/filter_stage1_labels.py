#!/usr/bin/env python3
"""Filter stage1_labels.jsonl by field values and write matches as JSONL.

Reads a JSONL label file, keeps the records that satisfy every supplied
constraint (constraints are AND-ed together), and writes the survivors to a
target file in the same JSONL format.

Available fields (from stage1_labels.jsonl):
    schema_version, domain, evaluation_split, label, confidence,
    labeler_id, labeled_at, source, notes  -- scalar fields
    rationale_keywords                      -- list field

Constraint kinds (all repeatable, AND-ed across the set):
    -f/--filter  FIELD=V[,V...]   keep if FIELD equals one of the values.
                                  For a list field (rationale_keywords) keep
                                  if the list overlaps the values (any-match,
                                  or all-match with --match-all).
    -x/--exclude FIELD=V[,V...]   drop if FIELD equals one of the values
                                  (list field: drop on any overlap).
    -c/--contains FIELD=SUBSTR    keep if SUBSTR (case-insensitive) appears in
                                  the field's text -- handy for notes/domain.

Comma-separated values within one constraint are OR-ed.

Examples:
    # All business rows in the train split, written to a new file.
    filter_stage1_labels.py -f label=business -f evaluation_split=train -o train_biz.jsonl

    # Non-business rows tagged software_product.
    filter_stage1_labels.py -f label=non-business -f rationale_keywords=software_product -o out.jsonl

    # Everything labeled by rommel_g that mentions "hospitality" in notes.
    filter_stage1_labels.py -f labeler_id=rommel_g -c notes=hospitality -o out.jsonl

    # Discover the fields and value distributions without writing anything.
    filter_stage1_labels.py --list-fields
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

DEFAULT_INPUT = Path(
    "/Users/administrator/projects/barcada-scraper/eval_data/stage1_labels.jsonl"
)


def parse_constraint(raw: str, *, sep: str = "=") -> tuple[str, list[str]]:
    """Split 'FIELD=V1,V2' into ('FIELD', ['V1', 'V2'])."""
    if sep not in raw:
        raise argparse.ArgumentTypeError(
            f"expected FIELD{sep}VALUE, got {raw!r}"
        )
    field, _, values = raw.partition(sep)
    field = field.strip()
    if not field:
        raise argparse.ArgumentTypeError(f"missing field name in {raw!r}")
    return field, [v.strip() for v in values.split(",") if v.strip()]


def field_values(record: dict, field: str) -> list[str]:
    """Return the record's value(s) for a field as a list of strings."""
    value = record.get(field)
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def matches(record: dict, args: argparse.Namespace) -> bool:
    """True if the record satisfies every constraint."""
    for field, wanted in args.filter or []:
        present = set(field_values(record, field))
        want = set(wanted)
        if args.match_all:
            if not want.issubset(present):
                return False
        elif present.isdisjoint(want):
            return False

    for field, unwanted in args.exclude or []:
        if not set(field_values(record, field)).isdisjoint(unwanted):
            return False

    for field, substrings in args.contains or []:
        haystack = " ".join(field_values(record, field)).lower()
        if not all(sub.lower() in haystack for sub in substrings):
            return False

    return True


def read_records(path: Path):
    """Yield (line_number, record) for each non-blank JSONL line."""
    with path.open() as f:
        for n, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield n, json.loads(line)
            except json.JSONDecodeError as exc:
                sys.exit(f"error: {path}:{n}: invalid JSON: {exc}")


def list_fields(path: Path) -> None:
    """Print each field with its value distribution and exit."""
    scalar: dict[str, Counter] = {}
    lists: dict[str, Counter] = {}
    total = 0
    for _, record in read_records(path):
        total += 1
        for key, value in record.items():
            if isinstance(value, list):
                bucket = lists.setdefault(key, Counter())
                bucket.update(str(v) for v in value)
            else:
                bucket = scalar.setdefault(key, Counter())
                bucket[str(value)] += 1

    print(f"{path}  ({total} records)\n")
    for key, counts in scalar.items():
        print(f"{key}  (scalar, {len(counts)} unique)")
        if len(counts) <= 20:
            for value, n in counts.most_common():
                print(f"    {value!r}: {n}")
        else:
            print(f"    high-cardinality, e.g. {list(counts)[:3]}")
    for key, counts in lists.items():
        print(f"{key}  (list, {len(counts)} unique)")
        for value, n in counts.most_common(20):
            print(f"    {value!r}: {n}")
        if len(counts) > 20:
            print(f"    ... and {len(counts) - 20} more")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i", "--input", type=Path, default=DEFAULT_INPUT,
        help=f"source JSONL file (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "-o", "--output", type=Path,
        help="destination JSONL file for matched records",
    )
    parser.add_argument(
        "-f", "--filter", action="append", type=parse_constraint, metavar="FIELD=V[,V]",
        help="keep records whose FIELD matches one of the values (repeatable)",
    )
    parser.add_argument(
        "-x", "--exclude", action="append", type=parse_constraint, metavar="FIELD=V[,V]",
        help="drop records whose FIELD matches one of the values (repeatable)",
    )
    parser.add_argument(
        "-c", "--contains", action="append", type=parse_constraint, metavar="FIELD=SUBSTR",
        help="keep records where SUBSTR appears in FIELD, case-insensitive (repeatable)",
    )
    parser.add_argument(
        "--match-all", action="store_true",
        help="for list-field --filter, require ALL listed values to be present",
    )
    parser.add_argument(
        "--list-fields", action="store_true",
        help="print available fields and value distributions, then exit",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="report how many records would match without writing output",
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="allow overwriting an existing output file",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.input.is_file():
        sys.exit(f"error: input file not found: {args.input}")

    if args.list_fields:
        list_fields(args.input)
        return 0

    if not (args.filter or args.exclude or args.contains):
        sys.exit("error: no constraints given (use -f/-x/-c, or --list-fields)")

    if not args.dry_run:
        if args.output is None:
            sys.exit("error: --output is required (or use --dry-run)")
        if args.output.exists() and not args.overwrite:
            sys.exit(f"error: {args.output} exists (pass --overwrite to replace)")
        if args.output.resolve() == args.input.resolve():
            sys.exit("error: refusing to overwrite the input file")

    total = matched = 0
    out = None
    if not args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        out = args.output.open("w")

    try:
        for _, record in read_records(args.input):
            total += 1
            if matches(record, args):
                matched += 1
                if out is not None:
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
    finally:
        if out is not None:
            out.close()

    where = "would match" if args.dry_run else f"-> {args.output}"
    print(f"{matched}/{total} records matched  {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
