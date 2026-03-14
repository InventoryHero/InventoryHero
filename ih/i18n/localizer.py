# ih/i18n/localizer.py
import json
import os
from functools import lru_cache
from typing import Any, Dict
from pathlib import Path
from fastapi import Header, Request

BASE_PATH = Path(__file__).parent.parent / "locales"

class Localizer:
    def __init__(self, locale: str = "en", fallback_locale: str = "en"):
        self.locale = locale
        self.fallback_locale = fallback_locale
        self._messages = self._load_locale(locale)
        self._fallback_messages = (
            self._load_locale(fallback_locale) if locale != fallback_locale else {}
        )

    @staticmethod
    @lru_cache(maxsize=None)
    def _load_locale(locale: str) -> Dict[str, Any]:
        """Load and cache locale JSON file"""
        file_path = BASE_PATH / f"{locale}.json"
        if not file_path.exists():
            return {}
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)

    def t(self, key: str, **kwargs) -> str:
        """
        Get a translation by key (dot notation supported)
        Example: localizer.t("errors.cannot_delete_self")
        """
        value = self._resolve_key(self._messages, key)
        if value is None:
            value = self._resolve_key(self._fallback_messages, key)
        if value is None:
            # Return key if not found (like StringLocalizer)
            return key
        return value.format(**kwargs) if kwargs else value

    def _resolve_key(self, data: Dict[str, Any], key: str):
        """Traverse nested keys (e.g., errors.cannot_delete_self)"""
        current = data
        for part in key.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(part)
            if current is None:
                return None
        return current


def get_localizer(request: Request) -> Localizer:
    # Parse the first language, e.g., "de-DE,de;q=0.9,en;q=0.8"
    lang = request.headers.get('accept-language', 'en')
    return Localizer(locale=lang)