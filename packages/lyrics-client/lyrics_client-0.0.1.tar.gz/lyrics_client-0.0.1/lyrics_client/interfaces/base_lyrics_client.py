from typing import List
from taipan_di import PipelineLink
from lyrics_client.classes import FetchLyricsCommand, FetchLyricsResult

__all__ = ["BaseLyricsClient"]

BaseLyricsClient = PipelineLink[FetchLyricsCommand, List[FetchLyricsResult]]