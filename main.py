from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve assets from a source directory based on reference files."
    )

    parser.add_argument(
        "--reference-dir",
        required=True,
        type=Path,
        help="Directory containing reference files (keys are derived from these).",
    )

    parser.add_argument(
        "--source-dir",
        required=True,
        type=Path,
        help="Directory containing source assets to resolve from.",
    )

    parser.add_argument(
        "--dest-dir",
        required=True,
        type=Path,
        help="Destination directory for resolved assets.",
    )

    parser.add_argument(
        "--reference-ext",
        nargs="+",
        default=[".png"],
        help="Reference file extensions (default: .png).",
    )

    parser.add_argument(
        "--source-ext",
        nargs="+",
        default=[".jpg", ".jpeg"],
        help="Source file extensions (default: .jpg .jpeg).",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without copying files.",
    )

    return parser.parse_args()


def normalise_extensions(exts: Iterable[str]) -> Set[str]:
    return {e.lower() if e.startswith(".") else f".{e.lower()}" for e in exts}


def index_source_files(
    source_dir: Path,
    source_exts: Set[str],
) -> Dict[str, Path]:
    """
    Build an index mapping base filenames to full source paths.
    """
    index: Dict[str, Path] = {}

    for file in source_dir.iterdir():
        if not file.is_file():
            continue

        if file.suffix.lower() in source_exts:
            index[file.stem] = file

    return index


def resolve_assets(
    reference_dir: Path,
    reference_exts: Set[str],
    source_index: Dict[str, Path],
) -> Tuple[List[Path], List[str]]:
    """
    Resolve reference files to source assets.
    Returns (resolved_paths, missing_keys).
    """
    resolved: List[Path] = []
    missing: List[str] = []

    for file in reference_dir.iterdir():
        if not file.is_file():
            continue

        if file.suffix.lower() not in reference_exts:
            continue

        key = file.stem
        if key in source_index:
            resolved.append(source_index[key])
        else:
            missing.append(key)

    return resolved, missing


def copy_assets(
    assets: Iterable[Path],
    destination_dir: Path,
    dry_run: bool = False,
) -> None:
    destination_dir.mkdir(parents=True, exist_ok=True)

    for asset in assets:
        dest = destination_dir / asset.name
        if dry_run:
            print(f"[DRY RUN] {asset} -> {dest}")
        else:
            shutil.copy2(asset, dest)


def main() -> None:
    args = parse_args()

    reference_exts = normalise_extensions(args.reference_ext)
    source_exts = normalise_extensions(args.source_ext)

    source_index = index_source_files(args.source_dir, source_exts)
    resolved, missing = resolve_assets(
        args.reference_dir,
        reference_exts,
        source_index,
    )

    copy_assets(resolved, args.dest_dir, dry_run=args.dry_run)

    print(f"Resolved assets: {len(resolved)}")
    print(f"Missing assets: {len(missing)}")

    if missing:
        print("Unresolved keys:")
        for key in missing:
            print(" -", key)


if __name__ == "__main__":
    main()