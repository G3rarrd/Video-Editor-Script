from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VideoContext:
    path: Path
    duration: float