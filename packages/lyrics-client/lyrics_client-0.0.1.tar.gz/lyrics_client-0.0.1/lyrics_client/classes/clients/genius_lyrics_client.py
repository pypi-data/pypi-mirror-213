from typing import Dict, List
from bs4 import BeautifulSoup
import requests

from lyrics_client.classes import FetchLyricsCommand
from lyrics_client.classes.clients import AbstractLyricsClient
from lyrics_client.errors import BadFormatError

__all__ = ["GeniusLyricsClient"]


class GeniusLyricsClient(AbstractLyricsClient):
    GENIUS_SEARCH_URL = "https://api.genius.com/search"
    GENIUS_SONG_URL = "https://api.genius.com/songs"
    GENIUS_REQUEST_TIMEOUT = 10

    def __init__(self) -> None:
        super().__init__()

        self.headers.update(
            {
                "Authorization": "Bearer "
                "-1Zo4VdAbOXzMheWulMIJJqtic0qFixSIavn9Yul2MjmexGxLO6WZokyH4PmweBC",
            }
        )
        
    @property
    def client_name(self) -> str:
        return "genius"

    def search_songs(self, request: FetchLyricsCommand) -> Dict[str, str]:
        search_query = f"{request.song_title} {request.song_artists}"

        response = requests.get(
            self.GENIUS_SEARCH_URL,
            params={"q": search_query},
            headers=self.headers,
            timeout=self.GENIUS_REQUEST_TIMEOUT,
        )

        results: Dict[str, str] = {}
        
        for hit in response.json()["response"]["hits"]:
            results[hit["result"]["full_title"]] = f"{self.GENIUS_SONG_URL}/{hit['result']['id']}"

        return results

    def fetch_lyrics(self, url: str) -> str:
        song_response = requests.get(url, headers=self.headers, timeout=10)
        
        song_url = song_response.json()["response"]["song"]["url"]
        genius_page_response = requests.get(song_url, headers=self.headers, timeout=10)

        soup = BeautifulSoup(
            genius_page_response.text.replace("<br/>", "\n"), "html.parser"
        )
        
        lyrics_div = soup.select_one("div.lyrics")
        lyrics_containers = soup.select("div[class^=Lyrics__Container]")

        # Get lyrics
        if lyrics_div:
            lyrics = lyrics_div.get_text()
        elif lyrics_containers:
            lyrics = "\n".join(con.get_text() for con in lyrics_containers)
        else:
            raise BadFormatError("Couldn't fetch the lyrics because the response had a bad format")

        if not lyrics:
            raise BadFormatError("Couldn't fetch the lyrics because the response had a bad format")

        # Clean lyrics
        lyrics = lyrics.strip()

        # Remove desc at the beginning if it exists
        for to_remove in ["desc", "Desc"]:
            lyrics.replace(to_remove, "", 1)

        return lyrics
        