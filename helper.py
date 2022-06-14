#!/usr/bin/env python3

import json
import os
import datetime
import random
import helper_extras
import warnings
import newsapi


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
        news_data_all: Dict of the API response object.
        news_data: List of dicts from the response object's 'articles' field.
        HOME: OS-dependent "HOME" filepath.
        API_DEFAULT: API key name lookup failure fallback.

    Local keys file must conform to the following format:
    [{'api': "newsapi", 'apikey': "your_key_here"}]
    """

    HOME = os.getenv("HOME", "")
    API_DEFAULT = "newsapi"

    @staticmethod
    def _is_list_of_dicts(candidate) -> bool:
        return bool(
            candidate
            and type(candidate) is list
            and all(type(item) is dict for item in candidate)
        )

    @staticmethod
    def _get_txt_filename(path: str, path_counter: int | str) -> str:
        return path + str(path_counter) + ".txt"

    @staticmethod
    def _get_json_filename(path: str, path_counter: int | str) -> str:
        return path + str(path_counter) + ".json"

    @staticmethod
    def _get_day(prev_days: int) -> str:
        """Takes in an integer and returns the date that many
        days before today as a string in ISO format (YYYY-MM-DD).

        Args:
            prev_days: The number of days before today.

        Returns:
            String of the date prev_days before today in ISO format.
        """
        today = datetime.date.today()
        td = datetime.timedelta(days=prev_days)
        day = today - td
        return day.isoformat()

    def __init__(
        self,
        news_path_base: str = os.path.join(HOME, "news_sample"),
        keys_path: str = os.path.join(HOME, "news_keys.json"),
        debug_path_base: str = os.path.join(HOME, "news_debug"),
        use_saved: bool = False,
    ) -> None:
        self.news_path_base = news_path_base
        self.keys_path = keys_path
        self.debug_path_base = debug_path_base
        self.news_data: list[dict] = []
        self.news_data_all: dict = {}
        if not use_saved:
            self._set_keys()

    def _set_keys(self) -> None:
        """Set this object's news_keys attribute to the read data from the local
        file containing news API keys at the path specified in this object's
        keys_path attribute.

        Raises:
            NewsKeysException: If the API keys file data is not a list of dicts.
            OSError: If raised by _read_json_file_keys when reading keys file.
        """
        self.news_keys = self._read_json_file_keys(self.keys_path)
        if not self._is_list_of_dicts(self.news_keys):
            raise helper_extras.NewsKeysException("list_of_dicts")

    def _get_keys(self) -> list[dict]:
        return (type(self.news_keys) is list and self.news_keys) or [{}]

    def _get_key_from_file(self, api: str) -> dict | None:
        """Takes in the name of a news API and returns the dict
        from the local keys file (self.news_keys) that corresponds
        to that name, assuming the keys file is in the required format.

        Args:
            api: The name of the news API.

        Returns:
            The dict corresponding to api or None if api is not found.

        Raises:
            TypeError: If the return value of _get_news_keys is not iterable.
            (This shouldn't happen because of how _get_keys is written.)
        """
        return next((a for a in self._get_keys() if a.get("api") == api), None)

    def _set_news_key_choice(self, api_name: str):
        """Takes in the name of a news API and sets this object's 'news_key_choice'
        attribute to the corresponding key in the local keys file.
        Assumes that the keys file conforms to the required format.
        Searches for the default API if the name is not found.
        Sets 'news_key_choice' to None if default is not found.

        Args:
            api: The name of the news API.

        Raises:
            NewsKeysException: If chosen API name or default not found in 'news_keys'.
        """
        news_key_dict = self._get_key_from_file(api_name) or self._get_key_from_file(
            self.API_DEFAULT
        )
        self.news_key_choice = news_key_dict and news_key_dict.get("apikey")
        try:
            if not self.news_key_choice:
                raise helper_extras.NewsKeysException()
        except helper_extras.NewsException:
            print("Could not find dict with chosen API name or default ('newsapi').")
            raise

    def set_news_from_newsapi(
        self,
        top: bool = True,
        lang: str = "en",
        query: str = "",
        prev_days: int = 0,
        sort_pop: bool = True,
    ) -> None:
        """Queries "newsapi" API and saves response to helper.news.

        Uses the key from local keys file associated with "newsapi"
        e.g. {'api': "newsapi", 'apikey': "your_key_here"}

        Args:
            top: Boolean to choose "top headlines" or "everything" endpoint.
            lang: String of the 2-letter ISO-639-1 language code. Options:
            query: String to search for articles (only used if top is False).
            prev_days: Number of days before today to get news from. Default: 0.
            sort_pop: Boolean to sort results by popularity or relevance (if top False).

        Raises:
            NewsKeysException: If self._set_news_key_choice() fails.
            NewsLangException: If lang not in lang options.

        lang options: ar de en es fr he it nl no pt ru se ud zh
        Advanced query options: https://newsapi.org/docs/endpoints/everything
        """
        self._set_news_key_choice("newsapi")
        newsapi_client = newsapi.NewsApiClient(self.news_key_choice)
        if lang not in helper_extras.LANG_OPTIONS:
            warnings.warn(
                "lang must be one of: ar de en es fr he it nl no pt ru se ud zh\ndefaulting to en"
            )
        if top:
            response = newsapi_client.get_top_headlines(
                category="general", language=lang
            )
        else:
            default_queries = ["covid", "climate", "china", "ukraine", "war"]
            query = query or random.choice(default_queries)
            sort = (sort_pop and "popularity") or "relevancy"
            day = self._get_day(prev_days)
            response = newsapi_client.get_everything(
                q=query, from_param=day, sort_by=sort, language=lang
            )
        self._set_news_data(response)

    def set_news_from_newsapi_file(self, path_counter: int | str = "") -> None:
        """Sets self.news_data to the parsed JSON from a local file
        containing a newsapi response object.
        """
        self._set_news_data(
            self._read_json_file_newsapi(
                self._get_json_filename(self.news_path_base, path_counter)
            )
        )

    def _set_news_data(self, data) -> None:
        # TODO: Pass string to Exception objects instead of using the print statements.
        try:
            if type(data) is dict:
                self.news_data_all = data
                news = self.news_data_all.get("articles") or []
                if self._is_list_of_dicts(news):
                    self.news_data = news
                else:
                    print(
                        "articles field of newsapi response object must be a list of dicts."
                    )
                    raise helper_extras.NewsDataException()
            else:
                print("newsapi response object must be a dict.")
                raise helper_extras.NewsDataException()
        except helper_extras.NewsException:
            raise

    def get_news_data(self) -> list[dict]:
        # TODO: Pass string to Exception objects instead of using the print statements.
        try:
            if self.news_data:
                return self.news_data
            raise helper_extras.NewsDataException()
        except helper_extras.NewsException:
            print(
                "News not set. Call set_news_from_newsapi or set_news_from_newsapi_file first."
            )
            raise

    def get_news_data_all(self) -> dict:
        # TODO: Pass string to Exception objects instead of using the print statements.
        try:
            if self.news_data_all:
                return self.news_data_all
            raise helper_extras.NewsDataException()
        except helper_extras.NewsException:
            print(
                "News not set. Call set_news_from_newsapi or set_news_from_newsapi_file first."
            )
            raise

    def save_news(self, path_counter: int | str = "") -> None:
        self._write_json_file(
            self.news_path_base, path_counter, self.get_news_data_all()
        )

    def save_debug_json(
        self, data: dict | list | object, path_counter: int | str = ""
    ) -> None:
        # TODO: Create exception for if the data is not a dict, list, or object.
        if type(data) is list or type(data) is dict:
            self._write_json_file(self.debug_path_base, path_counter, data)
        elif isinstance(data, object):
            self._write_json_file(
                self.debug_path_base, path_counter, data, helper_extras.NewsDebugEncoder
            )

    def save_debug_txt(self, data, path_counter: int | str = "") -> None:
        self._write_txt_file(self.debug_path_base, path_counter, data)

    def _write_json_file(
        self, path: str, path_counter, data: dict | list | object, encoder=None
    ) -> None:
        """
        Writes a dict, list, or class instance as json to a local file.
        To write a class instance, pass NewsDebugEncoder to encoder param.

        Args:
            path: The filepath to write to.
            data: The data to write.
            encoder: The encoder class to use to convert a class instance to JSON.

        Raises:
            TODO
        """
        # TODO: try/catch OSError
        with open(
            self._get_json_filename(path, path_counter), "w", encoding="utf-8"
        ) as f:
            json.dump(data, f, ensure_ascii=False, cls=encoder)

    def _write_txt_file(self, path, path_counter: int | str, data) -> None:
        # TODO: try/catch OSError
        with open(self._get_txt_filename(path, path_counter), "w") as f:
            f.write(data)

    def _read_json_file_newsapi(self, path: str) -> dict:
        """Reads and returns the contents of the JSON file at :path: param.
        Return type is dict to match the format of the 'newsapi' response object.

        Args:
            path: The filepath to read from.

        Returns:
            A dict of the news data.

        Raises:
            TODO:
        """
        # TODO: try/catch OSError
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _read_json_file_keys(self, path: str) -> list:
        """Reads and returns the contents of the JSON file at :path: param.
        Return type is list to match the format of the news keys file.

        Args:
            path: The filepath to read from.

        Returns:
            A list of file key dict(s).

        Raises:
            TODO
        """
        # TODO: try/catch OSError
        with open(path, encoding="utf-8") as f:
            return json.load(f)


def main():
    h = Helper()
    h.set_news_from_newsapi()
    h.save_news()


if __name__ == "__main__":
    main()
