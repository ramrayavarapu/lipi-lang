#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

import lipi
from lipi_v2.errors import V2LipiError
from lipi_v2.localization import format_v2_error
from lipi_v2.normalizer import normalize_source
from lipi_v2.pipeline import run_v2_source
from lipi_v2 import executor as v2_executor


@contextmanager
def captured_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


class TestV2RuntimePipeline(unittest.TestCase):
    def test_mixed_language_execution_with_symbol_alias(self):
        source = """
మార్కులు = 80
if marks > 75:
    చెప్పు "Distinction"
end
""".strip()

        with captured_output() as output:
            result = run_v2_source(source, lang='en')

        self.assertIn("Distinction", output.getvalue())
        self.assertIn("మార్కులు", result["env"])
        self.assertEqual(result["env"]["మార్కులు"], 80)

    def test_first_defined_wins_policy(self):
        source = """
marks = 90
యెడల మార్కులు > 75:
    print "Top"
end
""".strip()

        with captured_output() as output:
            result = run_v2_source(source, lang='en')

        self.assertIn("Top", output.getvalue())
        self.assertIn("marks", result["env"])
        self.assertNotIn("మార్కులు", result["env"])

    def test_first_defined_wins_policy_telugu_defined_first(self):
        source = """
మార్కులు = 90
if marks > 75:
    చెప్పు "Top"
end
""".strip()

        with captured_output() as output:
            result = run_v2_source(source, lang='en')

        self.assertIn("Top", output.getvalue())
        self.assertIn("మార్కులు", result["env"])
        self.assertNotIn("marks", result["env"])

    def test_malformed_block_validation(self):
        source = """
if 1 < 2:
    print "x"
""".strip()
        with self.assertRaises(V2LipiError) as err:
            run_v2_source(source)
        self.assertEqual(err.exception.key, "malformed_block")

    def test_localized_variable_error_telugu(self):
        err = V2LipiError("variable_not_defined", "marks", line=3)
        msg = format_v2_error(err, lang="te")
        self.assertIn("వేరియబుల్", msg)

    def test_negative_literal_assignment_supported(self):
        source = """
x = -1
print x
""".strip()
        with captured_output() as output:
            result = run_v2_source(source, lang="en")
        self.assertEqual(result["env"]["x"], -1)
        self.assertIn("-1", output.getvalue())

    def test_unsafe_tokens_inside_strings_are_allowed(self):
        source = 'print "eval(__import__(\\"os\\"))"\n'
        with captured_output() as output:
            run_v2_source(source, lang="en")
        self.assertIn('eval(__import__("os"))', output.getvalue())

    def test_unsupported_for_block_fails_validation(self):
        source = """
for item in 1:
    print item
end
""".strip()
        with self.assertRaises(V2LipiError) as err:
            run_v2_source(source, lang="en")
        self.assertEqual(err.exception.key, "malformed_block")

    def test_unsupported_compare_includes_line_context(self):
        source = """
y = 1
print y in y
""".strip()
        with self.assertRaises(V2LipiError) as err:
            run_v2_source(source, lang="en")
        self.assertEqual(err.exception.key, "type_error")
        self.assertEqual(err.exception.line, 2)

    def test_normalizer_respects_explicit_empty_keyword_map(self):
        source = "యెడల x > 0:\nend"
        normalized = normalize_source(source, keyword_map={})
        self.assertEqual(normalized.normalized_lines[0], "యెడల x > 0:")

    def test_loop_limit_env_invalid_falls_back_to_default(self):
        old = os.environ.get("LIPI_V2_MAX_LOOP_ITERATIONS")
        try:
            os.environ["LIPI_V2_MAX_LOOP_ITERATIONS"] = "not-an-int"
            self.assertEqual(
                v2_executor._resolve_max_loop_iterations(),
                v2_executor.DEFAULT_MAX_LOOP_ITERATIONS,
            )
        finally:
            if old is None:
                os.environ.pop("LIPI_V2_MAX_LOOP_ITERATIONS", None)
            else:
                os.environ["LIPI_V2_MAX_LOOP_ITERATIONS"] = old


class TestV2RuntimeCliIntegration(unittest.TestCase):
    def test_run_lipi_file_v2_mode_supports_lipi_extension(self):
        source = """
కౌంట్ = 1
while కౌంట్ <= 2:
    చెప్పు కౌంట్
    కౌంట్ = కౌంట్ + 1
end
""".strip()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.lipi', delete=False, encoding='utf-8') as f:
            f.write(source)
            path = f.name

        try:
            with captured_output() as output:
                lipi.run_lipi_file(path, mode='v2', lang='en')
            self.assertIn('1', output.getvalue())
            self.assertIn('2', output.getvalue())
        finally:
            os.unlink(path)

    def test_compat_mode_unchanged(self):
        source = 'print "Compat"\n'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lipi.py', delete=False, encoding='utf-8') as f:
            f.write(source)
            path = f.name

        try:
            with captured_output() as output:
                lipi.run_lipi_file(path, mode='compat', lang='en')
            self.assertIn('Compat', output.getvalue())
        finally:
            os.unlink(path)

    def test_compat_mode_applies_lang_argument_for_errors(self):
        source = "print missing_var\n"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lipi.py', delete=False, encoding='utf-8') as f:
            f.write(source)
            path = f.name

        try:
            with captured_output() as output:
                lipi.run_lipi_file(path, mode='compat', lang='te')
            self.assertIn("రన్‌టైమ్ లోపం", output.getvalue())
        finally:
            os.unlink(path)

    def test_run_command_cli_path_is_covered(self):
        source = """
count = 1
while count <= 2:
    print count
    count = count + 1
end
""".strip()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".lipi.py", delete=False, encoding="utf-8") as f:
            f.write(source)
            path = f.name

        try:
            proc = subprocess.run(
                [sys.executable, os.path.join(os.path.dirname(__file__), "..", "src", "lipi.py"), "run", path, "--mode", "v2", "--lang", "en"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertIn("1", proc.stdout)
            self.assertIn("2", proc.stdout)
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()
