from typing import Dict
from bs4 import BeautifulSoup
import requests

from lyrics_client.classes import FetchLyricsCommand
from lyrics_client.classes.clients import AbstractLyricsClient

__all__ = ["AZLyricsLyricsClient"]


class AZLyricsLyricsClient(AbstractLyricsClient):
    AZLYRICS_URL = "https://www.azlyrics.com/"
    AZLYRICS_GEO_URL = "https://www.azlyrics.com/geo.js"
    AZLYRICS_SEARCH_URL = "https://search.azlyrics.com/search.php"
    
    def __init__(self) -> None:
        super().__init__()
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        self.x_code = self._fetch_x_code()
        
    def _fetch_x_code(self) -> str:
        # First request to AZLyrics to load the geo.js file
        self.session.get(self.AZLYRICS_URL)
        geo = self.session.get(self.AZLYRICS_GEO_URL)
        
        # extract value from js code
        js_code = geo.text
        start_index = js_code.find('value"') + 9
        end_index = js_code[start_index:].find('");')

        return js_code[start_index : start_index + end_index]
        
    
    @property
    def client_name(self) -> str:
        return "azlyrics"

    def search_songs(self, request: FetchLyricsCommand) -> Dict[str, str]:
        params = {
            "q": f"{request.song_title} - {request.song_artists}",
            "x": self.x_code
        }
        
        search_response = self.session.get(self.AZLYRICS_SEARCH_URL, params=params)
        soup = BeautifulSoup(search_response.content, "html.parser")

        results: Dict[str, str] = {}
        td_tags = soup.find_all("td")
        
        for td_tag in td_tags:
            a_tags = td_tag.find_all("a", href=True)
            
            if len(a_tags) == 0 or a_tags[0]["href"].strip() == "":
                continue
            
            title_tag = td_tag.find("span")
            artist_tag = title_tag.find_next_sibling("b")
            
            title = title_tag.get_text().strip()
            artist = artist_tag.get_text().strip()
            url = a_tags[0]["href"].strip()
            
            results[f"{title} - {artist}"] = url
        
        return results
    
    def fetch_lyrics(self, url: str) -> str:
        song_response = self.session.get(url)
        soup = BeautifulSoup(song_response.content, "html.parser")

        # Find all divs that don't have a class or an id
        div_tags = soup.find_all("div", class_=False, id_=False)

        # Find the div with the longest text
        lyrics_div = sorted(div_tags, key=lambda x: len(x.text))[-1]

        # extract lyrics from div and clean it up
        lyrics = lyrics_div.get_text().strip()

        return lyrics
    