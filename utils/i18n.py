import json
from pathlib import Path

LOCALES_PATH = Path("locales")

class Translator:
    def __init__(self):
        self.locales = {}
        self.load_locales()

    def load_locales(self):
        for file in LOCALES_PATH.glob("*.json"):
            lang = file.stem
            with file.open("r", encoding="utf-8") as f:
                self.locales[lang] = json.load(f)

    def t(self, key: str, lang: str = "en") -> str:
        return self.locales.get(lang, {}).get(key, key)
