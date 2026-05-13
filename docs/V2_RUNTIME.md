# Lipi V2 Runtime Track

This document describes the new **V2 multilingual runtime pipeline** implemented as a separate track from the existing interpreter in `src/lipi.py`.

> **Naming note:** this “V2 runtime track” is an internal architecture track inside the current `v3.0` codebase. It is not a product version rollback.

## Scope

- V2 is a modular pipeline runtime.
- Existing interpreter remains the default **compatibility mode**.
- Internal canonical form is English keywords after normalization.
- Variable mapping policy is **first-defined wins** with alias tracking.

## Pipeline Modules

Located under `src/lipi_v2/`:

1. `dictionary.py` - deterministic keyword dictionary with versioning.
2. `normalizer.py` - Telugu/mixed source → canonical English keywords.
3. `symbol_mapper.py` - Telugu↔English symbol aliases, first-defined-wins canonical variable mapping.
4. `validator.py` - pre-execution validation for unsupported tokens and malformed blocks.
5. `ast_nodes.py` - AST model definitions.
6. `parser.py` - normalized lines → AST.
7. `executor.py` - AST interpreter runtime (no raw `exec`).
8. `debug_mapper.py` - Original ↔ Normalized ↔ AST mapping.
9. `localization.py` - EN/TE error localization catalog.
10. `pipeline.py` - orchestration layer.

## CLI usage

Backward-compatible mode (default):

```bash
python src/lipi.py examples/hello.lipi.py
```

V2 mode with `.lipi` or `.lipi.py`:

```bash
python src/lipi.py examples/hello.lipi.py --mode v2
python src/lipi.py run examples/hello.lipi.py --mode v2 --lang te
```

## Current coverage

Implemented in this runtime track:

- Deterministic normalization
- Symbol alias mapping and first-defined-wins policy
- Safe pre-execution validation
- AST parser and interpreter for core statements:
  - assignment
  - print
  - if/else/end
  - while/end
- Bilingual localized V2 error formatting
- Debug source mappings

## Notes

- V2 is introduced as a safe, incremental runtime path and does not replace compatibility mode.
- Existing tests and behavior of the current interpreter are preserved.
