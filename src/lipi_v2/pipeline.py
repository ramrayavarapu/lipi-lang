"""End-to-end V2 multilingual runtime pipeline."""

from .debug_mapper import DebugMapper
from .dictionary import KEYWORD_MAP, SYMBOL_SEED_MAP
from .errors import V2LipiError
from .executor import ExecutionEngine
from .localization import format_v2_error
from .normalizer import normalize_source
from .parser import Parser
from .symbol_mapper import SymbolMapper
from .validator import validate_normalized_lines


def _normalize_with_symbols(source: str, debug_mapper: DebugMapper):
    normalized = normalize_source(source, KEYWORD_MAP)
    symbol_mapper = SymbolMapper(seed_aliases=SYMBOL_SEED_MAP)

    transformed: list[str] = []
    for idx, line in enumerate(normalized.normalized_lines, start=1):
        stripped = line.strip()

        # First-defined-wins on assignment LHS.
        if "=" in stripped and not any(op in stripped for op in ("==", "!=", ">=", "<=")):
            lhs, rhs = stripped.split("=", 1)
            canonical = symbol_mapper.define_symbol(lhs.strip())
            rewritten = f"{canonical} = {rhs.strip()}"
            rewritten = symbol_mapper.normalize_identifiers_in_line(rewritten)
            leading = len(line) - len(line.lstrip())
            line = (" " * leading) + rewritten
        else:
            line = symbol_mapper.normalize_identifiers_in_line(line)

        transformed.append(line)
        debug_mapper.record_normalization(idx, source.splitlines()[idx - 1], line)

    return transformed, symbol_mapper


def run_v2_source(source: str, lang: str = "en") -> dict[str, object]:
    """Run V2 pipeline on source text and return environment."""
    debug_mapper = DebugMapper()

    try:
        normalized_lines, symbol_mapper = _normalize_with_symbols(source, debug_mapper)
        validate_normalized_lines(normalized_lines)
        program = Parser(debug_mapper=debug_mapper).parse(normalized_lines)
        engine = ExecutionEngine()
        env = engine.execute(program)
        return {
            "env": env,
            "symbol_mapper": symbol_mapper,
            "debug_mapper": debug_mapper,
        }
    except V2LipiError:
        raise
    except Exception as exc:
        raise V2LipiError("runtime_error", str(exc)) from exc


def run_v2_file(path: str, lang: str = "en") -> dict[str, object] | None:
    """Run V2 pipeline on a file and print localized errors."""
    with open(path, "r", encoding="utf-8") as handle:
        source = handle.read()

    try:
        return run_v2_source(source, lang=lang)
    except V2LipiError as err:
        # best-effort mapping with fresh mapper if unavailable
        print(format_v2_error(err, lang=lang))
        return None
