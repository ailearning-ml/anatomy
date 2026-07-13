from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List, Mapping

from .main import build_analysis, parse_input_documents, run_example, save_analysis, save_presentation


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="telecom-spec-dependency-slide-generator",
        description="Generate structured telecom specification dependency analysis output.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to a JSON file containing a list of telecom specification documents.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("examples") / "generated_analysis_output.json",
        help="Path to write the analysis JSON output.",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run the built-in example dataset instead of reading --input.",
    )
    parser.add_argument(
        "--pptx-output",
        type=Path,
        dest="pptx_output",
        help="Optional path to write a PowerPoint (.pptx) file in addition to JSON output.",
    )
    return parser


def load_payload(path: Path) -> List[Mapping[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Input JSON must contain a top-level list of document objects.")
    return data


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.example:
        result = run_example(args.output)
        print(f"Analysis written to {args.output}")
        if args.pptx_output:
            save_presentation(result, args.pptx_output)
            print(f"PowerPoint written to {args.pptx_output}")
        return 0

    if args.input is None:
        parser.error("Either --input must be provided or --example must be used.")

    payload = load_payload(args.input)
    documents = parse_input_documents(payload)
    result = build_analysis(documents)
    save_analysis(result, args.output)
    print(f"Analysis written to {args.output}")
    if args.pptx_output:
        save_presentation(result, args.pptx_output)
        print(f"PowerPoint written to {args.pptx_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
