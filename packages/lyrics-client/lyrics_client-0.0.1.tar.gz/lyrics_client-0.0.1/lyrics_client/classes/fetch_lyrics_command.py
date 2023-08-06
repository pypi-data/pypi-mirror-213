from dataclasses import dataclass, field
from typing import List

__all__ = ["FetchLyricsCommand"]

@dataclass
class FetchLyricsCommand:
    song_title: str
    song_artists: str
    clients: List[str] = field(default_factory=lambda: ["genius"])