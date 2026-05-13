#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

import lipi
from lipi_v2.errors import V2LipiError
from lipi_v2.localization import format_v2_error
from lipi_v2.pipeline import run_v2_source


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


if __name__ == '__main__':
    unittest.main()
