"""Deterministic normalization dictionary for V2."""

DICTIONARY_VERSION = "2.0.0"

# Keyword/constant normalization to canonical English internal form.
KEYWORD_MAP = {
    "చెప్పు": "print",
    "యెడల": "if",
    "లేకపోతే": "else",
    "వరకు": "while",
    "పునరావృతం": "for",
    "ముగింపు": "end",
    "కాల్": "call",
    "పనిచేయి": "function",
    "రిటర్న్": "return",
    "నిజం": "true",
    "అబద్ధం": "false",
    "శూన్యం": "null",
}

# Seed aliases used by symbol mapper for multilingual variable continuity.
SYMBOL_SEED_MAP = {
    "మార్కులు": "marks",
    "పేరు": "name",
    "వయసు": "age",
    "కౌంట్": "count",
    "సంఖ్య": "number",
    "మొత్తం": "total",
}

RESERVED_WORDS = {
    "if",
    "else",
    "while",
    "for",
    "function",
    "return",
    "print",
    "call",
    "end",
    "true",
    "false",
    "null",
}
