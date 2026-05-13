"""Symbol mapping with first-defined-wins alias policy."""

import re

from .dictionary import RESERVED_WORDS

IDENTIFIER_PATTERN = re.compile(r"[_\w\u0C00-\u0C7F]+", flags=re.UNICODE)


class SymbolMapper:
    """Tracks Telugu↔English symbol aliases with first-defined canonical selection."""

    def __init__(self, seed_aliases: dict[str, str] | None = None):
        self.seed_aliases = seed_aliases or {}
        self.alias_to_canonical: dict[str, str] = {}
        self.canonical_to_aliases: dict[str, set[str]] = {}
        self.group_to_canonical: dict[str, str] = {}

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
        if lang == "te":
            telugu = [a for a in aliases if any("\u0C00" <= c <= "\u0C7F" for c in a)]
            if telugu:
                return sorted(telugu)[0]
        if lang == "en":
            english = [a for a in aliases if all(not ("\u0C00" <= c <= "\u0C7F") for c in a)]
            if english:
                return sorted(english)[0]
        return canonical

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
                elif string_char == ch:
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
