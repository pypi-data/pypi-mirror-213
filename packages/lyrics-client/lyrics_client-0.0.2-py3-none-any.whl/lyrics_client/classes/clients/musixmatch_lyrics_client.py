from typing import Dict
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests

from lyrics_client.classes import FetchLyricsCommand
from lyrics_client.classes.clients import AbstractLyricsClient

__all__ = ["MusixmatchLyricsClient"]


class MusixmatchLyricsClient(AbstractLyricsClient):
    MUSIXMATCH_URL = "https://www.musixmatch.com"
    MUSIXMATCH_SEARCH_URL = "https://www.musixmatch.com/search"
    
    @property
    def client_name(self) -> str:
        return "musixmatch"

    def search_songs(self, request: FetchLyricsCommand) -> Dict[str, str]:
        query = quote(f"{request.song_title} - {request.song_artists}", safe="")
        results = self._search_musixmatch(query)

        if not results:
            # song_url_tag being None means no results were found on the
            # All Results page, therefore, we use `track_search` to
            # search the tracks page.
            results = self._search_musixmatch(f"{query}/tracks")

        return results

    def _search_musixmatch(self, query: str) -> Dict[str, str]:
        search_url = f"{self.MUSIXMATCH_SEARCH_URL}/{query}"

        search_response = requests.get(search_url, headers=self.headers, timeout=10)
        search_soup = BeautifulSoup(search_response.text, "html.parser")

        song_cards = search_soup.select("div.media-card-body")
        
        results: Dict[str, str] = {}

        for card in song_cards:
            title_tag = card.select_one("a.title[href^='/lyrics/']")
            artist_tag = card.select_one("a.artist")
            
            title = title_tag.get_text()
            artist = artist_tag.get_text()
            url = str(title_tag.get('href', ''))
            
            results[f"{title} - {artist}"] = f"{self.MUSIXMATCH_URL}{url}"

        return results

    def fetch_lyrics(self, url: str) -> str:
        lyrics_page = requests.get(url, headers=self.headers, timeout=10)

        lyrics_soup = BeautifulSoup(lyrics_page.text, "html.parser")
        lyrics_paragraphs = lyrics_soup.select("p.mxm-lyrics__content")
        lyrics = "\n".join(i.get_text() for i in lyrics_paragraphs)

        return lyrics
