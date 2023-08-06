from typing import List
from taipan_di import DependencyCollection

from lyrics_client.classes import FetchLyricsCommand, FetchLyricsResult
from lyrics_client.di import add_lyrics_client
from lyrics_client.interfaces import BaseLyricsClient

__all__ = ["LyricsClient"]


class LyricsClient:
    def __init__(self):
        services = DependencyCollection()
        add_lyrics_client(services)

        self._clients = services.build().resolve(BaseLyricsClient)

    def get_lyrics(self, request: FetchLyricsCommand) -> List[FetchLyricsResult]:
        return self._clients.exec(request)
    
    def get_from_song(self, song_title: str, song_artists: str, clients: List[str] = ["genius"]) -> List[FetchLyricsResult]:
        command = FetchLyricsCommand(song_title, song_artists, clients)
        return self._clients.exec(command)
        
