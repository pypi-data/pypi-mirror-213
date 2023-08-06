import abc
from typing import Callable, Dict, List, Tuple
from slugify import slugify
from rapidfuzz import fuzz

from lyrics_client.classes import FetchLyricsCommand, FetchLyricsResult
from lyrics_client.interfaces import BaseLyricsClient
from lyrics_client.errors import NoResultError, BadTitleMatchError

__all__ = ["AbstractLyricsClient"]


class AbstractLyricsClient(BaseLyricsClient, metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.headers = {
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Language": "en-US;q=0.8,en;q=0.7",
        }

    def _handle(
        self,
        request: FetchLyricsCommand,
        next: Callable[[FetchLyricsCommand], List[FetchLyricsResult]],
    ) -> List[FetchLyricsResult]:
        other_results = next(request) or []

        if self.client_name in request.clients:
            result = self.get_lyrics(request)
            other_results.append(result)

        return other_results

    def get_lyrics(self, request: FetchLyricsCommand) -> FetchLyricsResult:
        try:
            search_results = self.search_songs(request)
        except Exception as ex:
            return FetchLyricsResult(
                request.song_title, request.song_artists, self.client_name, None, ex
            )

        if not search_results:
            return FetchLyricsResult(
                request.song_title,
                request.song_artists,
                self.client_name,
                None,
                NoResultError(
                    f"No results found for song {request.song_title} by {request.song_artists}"
                ),
            )

        best_match = self.find_best_match(
            request.song_title, request.song_artists, search_results
        )

        if best_match[2] < 55:
            return FetchLyricsResult(
                request.song_title,
                request.song_artists,
                self.client_name,
                None,
                BadTitleMatchError(
                    "Best match found isn't close enough to your query. "
                    f"Best match : {best_match[0]}, query: {request.song_title} - {request.song_artists}"
                ),
            )

        try:
            lyrics = self.fetch_lyrics(best_match[1])

            return FetchLyricsResult(
                request.song_title, request.song_artists, self.client_name, lyrics
            )
        except Exception as ex:
            return FetchLyricsResult(
                request.song_title, request.song_artists, self.client_name, None, ex
            )

    def find_best_match(
        self, song_title: str, song_artists: str, search_results: Dict[str, str]
    ) -> Tuple[str, str, float]:
        best_score = 0
        best_url = ""
        best_title = ""

        song_slug = slugify(f"{song_title} - {song_artists}")

        for title, url in search_results.items():
            score = fuzz.ratio(slugify(title), song_slug)

            if score > best_score:
                best_score = score
                best_url = url
                best_title = title

        return best_title, best_url, best_score

    @property
    @abc.abstractmethod
    def client_name(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def search_songs(self, request: FetchLyricsCommand) -> Dict[str, str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def fetch_lyrics(self, url: str) -> str:
        raise NotImplementedError()
