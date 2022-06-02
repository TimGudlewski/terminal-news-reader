#!/usr/bin/env python3

import json
import os
import datetime
import random
from newsapi import NewsApiClient
from typing import Union


class Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Helper:
    """Access helper methods and define standard paths.

    Set file system paths to read API keys and write API response objects.
    Use helper methods to fetch from an API and save the response.

    Attributes:
    :news_path: String of the path to NEWS-FILE.
    :keys_path: String of the path to KEYS-FILE.
    :news_keys: List of dicts from KEYS-FILE.
    :news_key: String of the API key from KEYS-FILE.
    :news: Dict of the API response object.

    KEYS-FILE must be a JSON list of dicts w/k-v pairs:
    - api: A string of the API name.
    - apikey: A string of the API key.

    APIs currently supported: newsapi
    """

    home = os.getenv("HOME", "")

    def __init__(
        self,
        news_path: str = os.path.join(home, "news_sample.json"),
        keys_path: str = os.path.join(home, "news_keys.json"),
        get_keys: bool = True,
        debug_path: str = os.path.join(home, "nws_debug.json"),
        debug_path_alt: str = os.path.join(home, "news_debug_alt.txt"),
    ) -> None:
        self.news_path = news_path
        self.keys_path = keys_path
        self.debug_path = debug_path
        self.debug_path_alt = debug_path_alt
        if get_keys:
            self.news_keys = self._read_json_file_keys(self.keys_path)

    def _get_day(self, prev_days):
        today = datetime.date.today()
        td = datetime.timedelta(days=prev_days)
        day = today - td
        return day.isoformat()

    def _set_news_key(self, api):
        api_default = "newsapi"
        news_key_dict = next((a for a in self.news_keys if a.get("api") == api), None)
        self.news_key = (news_key_dict and news_key_dict.get("apikey")) or api_default

    def set_news_newsapi(
        self,
        top: bool = True,
        lang: str = "en",
        query: str = "",
        prev_days: int = 0,
        sortpop: bool = True,
    ) -> None:
        """Query "newsapi" and save response to Helper attr :news:

        Uses the key from KEYS-FILE associated with "newsapi".
        e.g. {"api": "newsapi", "apikey": "your_key_here"}

        Args:
        :top: Boolean to choose "top headlines" or "everything" endpoint.
        :lang: String of the 2-letter ISO-639-1 language code. Options:
        - ar de en es fr he it nl no pt ru se ud zh
        :query: String to search for articles (only used if :top: is False).
        - Adv. search opt's: https://newsapi.org/docs/endpoints/everything
        :prev_days: Number of days before today to get news from. 0 = today.
        - Default: 0
        :sortpop: Boolean to sort results by popularity or relevance
        - (only used if :top: is False).
        """
        self._set_news_key("newsapi")
        napic = NewsApiClient(self.news_key)
        if top:
            self.news = napic.get_top_headlines(category="general", language=lang)
        else:
            default_queries = ["covid", "climate", "china", "ukraine", "war"]
            query = query or random.choice(default_queries)
            sort = (sortpop and "popularity") or "relevancy"
            day = self._get_day(prev_days)
            self.news = napic.get_everything(
                q=query, from_param=day, sort_by=sort, language=lang
            )

    def set_news_file(self):
        self.news = self._read_json_file_news(self.news_path)

    def get_news(self) -> dict:
        return self.news

    def save_news(self, path_counter=""):
        self._write_json_file(self.news_path, path_counter, self.news)

    def save_debug_json(self, data, path_counter=""):
        if type(data) is list or type(data) is dict:
            self._write_json_file(self.debug_path, path_counter, data)
        elif isinstance(data, object):
            self._write_json_file(self.debug_path, path_counter, data, Encoder)

    def save_debug_txt(self, data, path_counter=""):
        self._write_txt_file(self.debug_path, path_counter, data)

    def _write_json_file(
        self, path: str, path_counter, data: Union[dict, list, object], encoder=None
    ) -> None:
        with open(self._get_json_filename(path, path_counter), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, cls=encoder)

    def _write_txt_file(self, path, data, path_counter):
        with open(self._get_txt_filename(path, path_counter), "w") as f:
            f.write(data)

    def _read_json_file_news(self, path: str) -> dict:
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _read_json_file_keys(self, path: str) -> list:
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _get_txt_filename(self, path: str, path_counter) -> str:
        return path + str(path_counter) + ".txt"

    def _get_json_filename(self, path: str, path_counter) -> str:
        return path + str(path_counter) + ".json"


def main():
    h = Helper()
    h.set_news_newsapi()
    h.save_news()


if __name__ == "__main__":
    main()
