import json


LANG_OPTIONS = [
    "ar",
    "de",
    "en",
    "es",
    "fr",
    "he",
    "it",
    "nl",
    "no",
    "pt",
    "ru",
    "se",
    "ud",
    "zh",
]


class NewsException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)


class NewsKeysException(NewsException):
    def __init__(self):
        super().__init__(
            "Failed to retrieve key(s) from local keys file. Please ensure proper formatting"
        )


class NewsDataException(NewsException):
    def __init__(self):
        super().__init__("Improperly formatted newsapi data.")


class NewsDebugEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
