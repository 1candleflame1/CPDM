from pathlib import Path
from shutil import copy2


def main():
    root = Path(__file__).resolve().parent
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp", ".gif"}
    pairs = {}
    for split in ("train", "test"):
        folder = root / "LSUI" / split / "input"
        if not folder.is_dir():
            raise SystemExit(f"Input directory not found: {folder}")
        pairs[split] = sorted(
            p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in extensions
        )

    missing = {p.name for files in pairs.values() for p in files
               if not (root / "GT" / p.name).is_file()}
    if missing:
        raise SystemExit("Missing GT files:\n" + "\n".join(sorted(missing)))

    for split, files in pairs.items():
        destination = root / "LSUI" / split / "GT"
        destination.mkdir(parents=True, exist_ok=True)
        for image in files:
            copy2(root / "GT" / image.name, destination / image.name)
        print(f"{split}: copied {len(files)} GT images to {destination}")


if __name__ == "__main__":
    main()
