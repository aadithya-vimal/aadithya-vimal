from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: python scripts/prep_photo.py <photo>")
        return

    source = Path(sys.argv[1])
    if not source.exists():
        raise SystemExit(f"photo not found: {source}")

    print(
        "Photo prep placeholder complete. "
        "This repo currently uses a bundled ASCII portrait source in assets/ascii-portrait.txt. "
        "Replace scripts/prep_photo.py with your preferred image-to-ascii pipeline when ready."
    )


if __name__ == "__main__":
    main()
