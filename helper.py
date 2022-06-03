#!/usr/bin/env python3

import json
import os
import datetime
import random
import helper_extras
from newsapi import NewsApiClient
from typing import Union


class Helper:
    """Fetches and saves news, saves debug dumps, and defines paths.

    Reads news API keys from a local file,
    fetches news API response objects to use as the data for NewsReader,
    writes news API response objects and portions thereof to a local file,
    writes program state dumps to a local file for debugging,
    and sets all the local file paths relevant to these behaviors.

    Attributes:
        news_path: String of the path to the local news file.
        keys_path: String of the path to the local keys file.
        news_keys: List of dicts from the keys file.
        news_key_choice: String of the chosen API key to use in fetch.
        news: Dict of the API response object.
        HOME: OS-dependent "HOME" filepath.
        API_DEFAULT: API key name lookup failure fallback.

    Local keys file must conform to the following format:
    [{'api': "newsapi", 'apikey': "your_key_here"}]
    """

    HOME = os.getenv("HOME", "")
    API_DEFAULT = "newsapi"

    def __init__(
        self,
        news_path: str = os.path.join(HOME, "news_sample.json"),
        keys_path: str = os.path.join(HOME, "news_keys.json"),
        get_keys: bool = True,
        debug_path: str = os.path.join(HOME, "news_debug.json"),
    ) -> None:
        self.news_path = news_path
        self.keys_path = keys_path
        self.debug_path = debug_path
        if get_keys:
            self.news_keys = self._read_json_file_keys(self.keys_path)

    def _get_day(self, prev_days: int) -> str:
        today = datetime.date.today()
        td = datetime.timedelta(days=prev_days)
        day = today - td
        return day.isoformat()

    def _get_key_from_file(self, api: str) -> Union[dict, None]:
        return next((a for a in self.news_keys if a.get("api") == api), None)

    def _set_news_key_choice(self, api_name: str):
        news_key_dict = self._get_key_from_file(api_name) or self._get_key_from_file(
            self.API_DEFAULT
        )
        self.news_key_choice = news_key_dict and news_key_dict.get("apikey")

    def set_news_from_newsapi(
        self,
        top: bool = True,
        lang: str = "en",
        query: str = "",
        prev_days: int = 0,
        sortpop: bool = True,
    ) -> None:
        """Queries "newsapi" API and saves response to helper.news.

        Uses the key from local keys file associated with "newsapi"
        e.g. {'api': "newsapi", 'apikey': "your_key_here"}

        Args:
            top: Boolean to choose "top headlines" or "everything" endpoint.
            lang: String of the 2-letter ISO-639-1 language code. Options:
            query: String to search for articles (only used if top is False).
            prev_days: Number of days before today to get news from. Default: 0.
            sortpop: Boolean to sort results by popularity or relevance (if top False).

        Raises:
            NewsKeyException: If self._set_news_key_choice() fails.
            NewsLangException: If lang not in lang options.

        lang options: ar de en es fr he it nl no pt ru se ud zh
        Advanced query options: https://newsapi.org/docs/endpoints/everything
        """
        self._set_news_key_choice("newsapi")
        try:
            if not self.news_key_choice:
                raise helper_extras.NewsKeyException()
            if lang not in helper_extras.LANG_OPTIONS:
                raise helper_extras.NewsLangException()
        except helper_extras.NewsException:
            raise
        newsapi_client = NewsApiClient(self.news_key_choice)
        if top:
            self.news = newsapi_client.get_top_headlines(
                category="general", language=lang
            )
        else:
            default_queries = ["covid", "climate", "china", "ukraine", "war"]
            query = query or random.choice(default_queries)
            sort = (sortpop and "popularity") or "relevancy"
            day = self._get_day(prev_days)
            self.news = newsapi_client.get_everything(
                q=query, from_param=day, sort_by=sort, language=lang
            )

    def set_news_from_file(self) -> None:
        self.news = self._read_json_file_news(self.news_path)

    def get_news(self) -> dict:
        return self.news

    def save_news(self, path_counter: Union[int, str] = "") -> None:
        self._write_json_file(self.news_path, path_counter, self.news)

    def save_debug_json(
        self, data: Union[dict, list, object], path_counter: Union[int, str] = ""
    ) -> None:
        if type(data) is list or type(data) is dict:
            self._write_json_file(self.debug_path, path_counter, data)
        elif isinstance(data, object):
            self._write_json_file(
                self.debug_path, path_counter, data, helper_extras.NewsDebugEncoder
            )

    def save_debug_txt(self, data, path_counter: Union[int, str] = "") -> None:
        self._write_txt_file(self.debug_path, data, path_counter)

    def _write_json_file(
        self, path: str, path_counter, data: Union[dict, list, object], encoder=None
    ) -> None:
        """
        Writes a dict, list, or class instance as json to a local file.
        To write a class instance, pass NewsDebugEncoder to encoder param.

        Args:
            path: The filepath to write to.
            data: The data to write.
            encoder: The encoder class to use to convert a class instance to JSON.
        """
        with open(
            self._get_json_filename(path, path_counter), "w", encoding="utf-8"
        ) as f:
            json.dump(data, f, ensure_ascii=False, cls=encoder)

    def _write_txt_file(self, path, data: str, path_counter: Union[int, str]) -> None:
        with open(self._get_txt_filename(path, path_counter), "w") as f:
            f.write(data)

    def _read_json_file_news(self, path: str) -> dict:
        """
        Reads and returns the contents of the JSON file at path param.
        Return type is dict to match the format of the "newsapi" response object.

        Args:
            path: The filepath to read from.
        Returns:
            A dict of the news data.
        Raises:
            FileNotFoundError: If file at path param is not found.
        """
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _read_json_file_keys(self, path: str) -> list:
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _get_txt_filename(self, path: str, path_counter: Union[int, str]) -> str:
        return path + str(path_counter) + ".txt"

    def _get_json_filename(self, path: str, path_counter: Union[int, str]) -> str:
        return path + str(path_counter) + ".json"


def main():
    h = Helper()
    h.set_news_from_newsapi()
    h.save_news()


if __name__ == "__main__":
    main()
