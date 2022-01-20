#!/usr/bin/env python3

import json
import os
import datetime
import random
from newsapi import NewsApiClient
from typing import Union


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
    def __init__(self, news_path: str = os.path.join(home, "news_sample.json"),
                       keys_path: str = os.path.join(home, "news_keys.json"),
                       get_keys: bool = True
    ) -> None:
        self.news_path = news_path
        self.keys_path = keys_path
        if get_keys:
            self.news_keys = self._read_json_file(self.keys_path)


    def _get_day(self, prev_days):
        today = datetime.date.today()
        td = datetime.timedelta(days=prev_days)
        day = today - td
        return day.isoformat()


    def _set_news_key(self, api):
        api_default = "newsapi"
        news_key_dict = next((a for a in self.news_keys if a.get("api") == api), None)
        self.news_key = (news_key_dict and news_key_dict.get("apikey")) or api_default


    def get_news_newsapi(self, top: bool = True,
                               lang: str = "en",
                               query: str = "",
                               prev_days: int = 0,
                               sortpop: bool = True
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
            news = napic.get_top_headlines(category="general", language=lang)
        else:
            default_queries = ["covid", "climate", "china", "ukraine", "war"]
            query = query or random.choice(default_queries)
            sort = (sortpop and "popularity") or "relevancy"
            day = self._get_day(prev_days)
            news = napic.get_everything(q=query, from_param=day, sort_by=sort, language=lang)
        self.news = news["articles"]


    def get_news_file(self):
        self.news = self._read_json_file(self.news_path)


    def save_news(self):
        self._write_json_file(self.news)


    def _write_json_file(self, data: Union[dict, list]) -> None:
        with open(self.news_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)


    def _read_json_file(self, path: str) -> Union[dict, list]:
        with open(path, encoding='utf-8') as f:
            return json.load(f)


def main():
    h = Helper()
    h.get_news_newsapi()
    h.save_news()


if __name__ == "__main__":
    main()

