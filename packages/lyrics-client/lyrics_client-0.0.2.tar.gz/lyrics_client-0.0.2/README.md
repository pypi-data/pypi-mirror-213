# Lyrics-Client

**Get the lyrics of your favorite musics !**

## Features

 - Automatic lyrics fetching from different services
    - Currently supported : Genius, Musixmatch, AZLyrics
 - Title and artist verification to find the best match
 - Easy to use, straightforward interface
 - Extensive results information
 - Possible to use via DI integration

## Installation

### Pip

```
pip install lyrics-client
```

### Poetry

[Poetry](https://python-poetry.org/) is a Python dependency management and packaging tool. I actually use it for this project.

```
poetry add lyrics-client
```

## Usage

There are 2 ways to use this library : using the LyricsClient object or via the DI.

### Using LyricsClient

The library exposes the LyricsClient class. This class has 2 methods : `get_lyrics` and `get_from_song`.

Both methods do the same thing : fetching lyrics and returns the results in a list of `FetchLyricsResult`.

However, `get_lyrics` accept a `FetchLyricsCommand` object as parameter, while `get_from_song` accept a song title, the song artists and optionally the clients to use.

**Example :**

```python
from lyrics_client import LyricsClient

client = LyricsClient()
results = client.get_from_song("in the end", "linkin park")

lyrics = results[0].lyrics
```

### Using DI

The library also exposes a `BaseLyricsClient` interface and a `add_lyrics_client` function for [Taipan-DI](https://github.com/Billuc/Taipan-DI).

In this method, the clients are registered as a Pipeline. All you need to do is to resolve the pipeline and execute it.

**Example :**

```python
from lyrics_client import BaseLyricsClient, add_lyrics_client, FetchLyricsCommand
from taipan_di import DependencyCollection

services = DependencyCollection()
add_lyrics_client(services)

provider = services.build()
client = provider.resolve(BaseLyricsClient)
request = FetchLyricsCommand("in the end", "linkin park")

results = client.exec(request)
lyrics = results[0].lyrics
```

## Inspirations

This library is partially based on spotDL's [spotify-downloader](https://github.com/spotDL/spotify-downloader).
