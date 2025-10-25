"""Package the visual identifier search example into a zip archive.

This helper script makes it easy to share the OCR/QR search example as a
single downloadable archive containing the Python script and the usage guide.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = EXAMPLE_DIR / "visual_identifier_search.py"
DOC_PATH = REPO_ROOT / "docs" / "visual-search-example.md"
DEFAULT_OUTPUT = EXAMPLE_DIR / "visual_identifier_search_example.zip"


def build_archive(destination: Path) -> None:
    if not SCRIPT_PATH.exists():
        raise FileNotFoundError(f"Example script not found: {SCRIPT_PATH}")
    if not DOC_PATH.exists():
        raise FileNotFoundError(f"Usage guide not found: {DOC_PATH}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(destination, mode="w", compression=ZIP_DEFLATED) as archive:
        archive.write(SCRIPT_PATH, arcname=SCRIPT_PATH.name)
        archive.write(DOC_PATH, arcname="visual-search-example.md")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a zip file containing the visual identifier search example"
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to the output zip archive (default: %(default)s)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(argv) if argv is not None else sys.argv[1:])
    output_path = Path(args.output).expanduser().resolve()

    build_archive(output_path)
    print(f"Created archive: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
