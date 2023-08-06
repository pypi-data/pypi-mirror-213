from dataclasses import dataclass

__all__ = ["FetchLyricsResult"]

@dataclass
class FetchLyricsResult:
    song_title: str
    song_artists: str
    client: str
    lyrics: str
    exception: Exception = None