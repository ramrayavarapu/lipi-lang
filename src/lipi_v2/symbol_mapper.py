"""Symbol mapping with first-defined-wins alias policy."""

import re

from .dictionary import RESERVED_WORDS
from .text_utils import transform_identifiers_outside_strings

TELUGU_CHAR_PATTERN = re.compile(r"[\u0C00-\u0C7F]")
GROUP_KEY_SEPARATOR = "::"


class SymbolMapper:
    """Tracks multilingual symbols using first-defined-wins canonicalization.

    The first encountered symbol in an alias group becomes canonical, and all
    known aliases (including seed aliases) resolve to that canonical name.
    """

    def __init__(self, seed_aliases: dict[str, str] | None = None):
        self.seed_aliases = seed_aliases or {}
        self.alias_to_canonical: dict[str, str] = {}
        self.canonical_to_aliases: dict[str, set[str]] = {}
        self.group_to_canonical: dict[str, str] = {}
        self.alias_language_cache: dict[str, str] = {}

    def _group_key(self, name: str) -> str | None:
        """Build deterministic alias-group key by sorting known seed alias pairs."""
        for left, right in self.seed_aliases.items():
            if name in (left, right):
                return GROUP_KEY_SEPARATOR.join(sorted((left, right)))
        return None

    def define_symbol(self, name: str) -> str:
        if name in RESERVED_WORDS:
            return name

        group_key = self._group_key(name)
        if name in self.alias_to_canonical:
            return self.alias_to_canonical[name]

        if group_key and group_key in self.group_to_canonical:
            canonical = self.group_to_canonical[group_key]
        else:
            canonical = name

        self.alias_to_canonical[name] = canonical
        self.canonical_to_aliases.setdefault(canonical, set()).add(name)

        if group_key:
            self.group_to_canonical[group_key] = canonical
            left, right = group_key.split(GROUP_KEY_SEPARATOR)
            for alias in (left, right):
                self.alias_to_canonical.setdefault(alias, canonical)
                self.canonical_to_aliases.setdefault(canonical, set()).add(alias)

        return canonical

    def resolve_reference(self, name: str) -> str:
        if name in RESERVED_WORDS:
            return name
        if name in self.alias_to_canonical:
            return self.alias_to_canonical[name]

        group_key = self._group_key(name)
        if group_key and group_key in self.group_to_canonical:
            canonical = self.group_to_canonical[group_key]
            self.alias_to_canonical[name] = canonical
            self.canonical_to_aliases.setdefault(canonical, set()).add(name)
            return canonical

        return name

    def preferred_alias(self, canonical: str, lang: str = "en") -> str:
        aliases = self.canonical_to_aliases.get(canonical, {canonical})
        alias_lang = {alias: self._alias_language(alias) for alias in aliases}
        if lang == "te":
            telugu = [a for a in aliases if alias_lang[a] == "te"]
            if telugu:
                return sorted(telugu)[0]
        if lang == "en":
            english = [a for a in aliases if alias_lang[a] == "en"]
            if english:
                return sorted(english)[0]
        return canonical

    def _alias_language(self, alias: str) -> str:
        if alias in self.alias_language_cache:
            return self.alias_language_cache[alias]
        language = "te" if TELUGU_CHAR_PATTERN.search(alias) else "en"
        self.alias_language_cache[alias] = language
        return language

    def normalize_identifiers_in_line(self, line: str) -> str:
        return transform_identifiers_outside_strings(line, self.resolve_reference)
