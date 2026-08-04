from pathlib import Path


def unique_output_path(directory: Path, filename: Path) -> Path:
    output = directory / filename

    counter = 1
    while output.exists():
        output = directory / f"{filename.stem}_{counter}{filename.suffix}"
        counter += 1

    return output