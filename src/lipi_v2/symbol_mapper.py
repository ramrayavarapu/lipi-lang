"""Symbol mapping with first-defined-wins alias policy."""

import re

from .dictionary import RESERVED_WORDS

IDENTIFIER_PATTERN = re.compile(r"[_\w\u0C00-\u0C7F]+", flags=re.UNICODE)
TELUGU_CHAR_PATTERN = re.compile(r"[\u0C00-\u0C7F]")


class SymbolMapper:
    """Tracks Telugu↔English symbol aliases with first-defined canonical selection."""

    def __init__(self, seed_aliases: dict[str, str] | None = None):
        self.seed_aliases = seed_aliases or {}
        self.alias_to_canonical: dict[str, str] = {}
        self.canonical_to_aliases: dict[str, set[str]] = {}
        self.group_to_canonical: dict[str, str] = {}
        self.alias_language_cache: dict[str, str] = {}

    def _group_key(self, name: str) -> str | None:
        for left, right in self.seed_aliases.items():
            if name in (left, right):
                return "::".join(sorted((left, right)))
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
            left, right = group_key.split("::")
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
        in_string = False
        string_char = None
        out = []
        i = 0

        while i < len(line):
            ch = line[i]
            if ch in {'"', "'"}:
                if not in_string:
                    in_string = True
                    string_char = ch
                elif string_char == ch and not self._is_escaped_quote(line, i):
                    in_string = False
                    string_char = None
                out.append(ch)
                i += 1
                continue

            if in_string:
                out.append(ch)
                i += 1
                continue

            match = IDENTIFIER_PATTERN.match(line, i)
            if not match:
                out.append(ch)
                i += 1
                continue

            token = match.group(0)
            canonical = self.resolve_reference(token)
            out.append(canonical)
            i = match.end()

        return "".join(out)

    @staticmethod
    def _is_escaped_quote(line: str, quote_index: int) -> bool:
        slashes = 0
        j = quote_index - 1
        while j >= 0 and line[j] == "\\":
            slashes += 1
            j -= 1
        return slashes % 2 == 1
