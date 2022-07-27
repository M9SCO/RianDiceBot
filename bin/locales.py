from os import listdir
from pathlib import Path
from typing import Any

from yaml import load, SafeLoader


def load_locales(path_str: str = "resources/texts/") -> dict[bytes, Any]:
    """
    :param path_str:
    :return:
    """
    locales = {}
    path: Path = Path(path_str)
    for i in listdir(path):
        locales[i.split(".")[0]] = load(Path(path / i).open(encoding="UTF-8"), Loader=SafeLoader, )
    return locales


def get_locale(key: str, lang: str, default: str | None = "[🟥]") -> dict | str:
    """
    :param key: str. path.to.str
    :param lang: str. user_lang
    :return:
    """

    match lang.lower():
        case "ru":
            l = lang
        case _:
            l = "en"

    path = key.split(".")
    locate = LOCALES[l]
    while path:
        locate = locate.get(path.pop(0))
        if not locate:
            return default
    return locate


LOCALES = load_locales()
