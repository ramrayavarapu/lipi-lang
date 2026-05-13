"""Localization catalog and error formatting for V2."""

from .errors import V2LipiError


ERROR_CATALOG = {
    "en": {
        "runtime_error": "Runtime error",
        "syntax_error": "Syntax error",
        "symbol_error": "Symbol error",
        "variable_not_defined": "Variable '{var}' not defined",
        "unsupported_token": "Unsupported token: {token}",
        "malformed_block": "Malformed block structure",
        "parser_error": "Parser error",
        "type_error": "Type error",
        "import_error": "Import error",
    },
    "te": {
        "runtime_error": "రన్‌టైమ్ లోపం",
        "syntax_error": "వాక్యనిర్మాణ లోపం",
        "symbol_error": "సింబల్ లోపం",
        "variable_not_defined": "వేరియబుల్ '{var}' నిర్వచించబడలేదు",
        "unsupported_token": "మద్దతు లేని టోకెన్: {token}",
        "malformed_block": "తప్పు బ్లాక్ నిర్మాణం",
        "parser_error": "పార్సర్ లోపం",
        "type_error": "రకం లోపం",
        "import_error": "దిగుమతి లోపం",
    },
}


def format_v2_error(error: V2LipiError, lang: str = "en", symbol_mapper=None) -> str:
    """Format a V2LipiError in selected language with identifier mapping."""
    catalog = ERROR_CATALOG.get(lang, ERROR_CATALOG["en"])
    prefix = "[లోపం]" if lang == "te" else "[Error]"
    template = catalog.get(error.key, error.key)

    detail = error.detail
    if error.key == "variable_not_defined" and symbol_mapper and detail:
        mapped = symbol_mapper.preferred_alias(detail, lang=lang)
        detail = mapped

    message = template.format(var=detail, token=detail)
    if error.key not in {"variable_not_defined", "unsupported_token"} and detail:
        message = f"{message}: {detail}"

    if error.line is not None:
        message = f"{message} (line {error.line})"

    return f"{prefix} {message}"
