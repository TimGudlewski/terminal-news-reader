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
    MESSAGES = {
        'list_of_dicts': "The keys file must be a JSON list of dicts."
    }
    def __init__(self, msg_type: str = ""):
        super().__init__(
            "Failed to retrieve key(s) from local keys file. Please ensure proper formatting.\n"
            + (self.MESSAGES.get(msg_type) or "")
        )


class NewsDataException(NewsException):
    def __init__(self, msg: str = ""):
        super().__init__("Improperly formatted newsapi data.\n" + msg)


class NewsDebugEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
