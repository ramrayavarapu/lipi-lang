"""
Baseline smoke tests for lipi-lang.
Verifies the interpreter can be imported and executes Telugu and English code correctly.
All PRs must maintain or extend this coverage.
"""
import sys
import os
import unittest
from io import StringIO
from contextlib import contextmanager

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import lipi


@contextmanager
def captured_output():
    buf = StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        yield buf
    finally:
        sys.stdout = old


class TestInterpreterSmoke(unittest.TestCase):
    """Confirms the interpreter is importable and executes basic programs."""

    def test_telugu_print(self):
        env = {}
        with captured_output() as out:
            lipi.run_lipi_line('చెప్పు "నమస్తే"', env)
        self.assertEqual(out.getvalue().strip(), "నమస్తే")

    def test_english_print(self):
        env = {}
        with captured_output() as out:
            lipi.run_lipi_line('print "Hello"', env)
        self.assertEqual(out.getvalue().strip(), "Hello")

    def test_variable_assignment_and_lookup(self):
        env = {}
        lipi.run_lipi_line('పేరు = "రాము"', env)
        self.assertEqual(env["పేరు"], "రాము")

    def test_arithmetic_expression(self):
        env = {"వయసు": 18}
        result = lipi.eval_lipi_expr('వయసు + 2', env)
        self.assertEqual(result, 20)

    def test_comparison_expression(self):
        env = {"వయసు": 20}
        self.assertTrue(lipi.eval_lipi_expr('వయసు >= 18', env))
        self.assertFalse(lipi.eval_lipi_expr('వయసు < 18', env))

    def test_telugu_if_block_true_branch(self):
        lines = ['యెడల 10 > 5:', '    చెప్పు "అవును"', 'ముగింపు']
        env = {}
        with captured_output() as out:
            lipi.run_lipi_if_block(lines, 0, env)
        self.assertIn("అవును", out.getvalue())

    def test_english_if_block_false_branch(self):
        lines = ['if 5 > 10:', '    print "wrong"', 'end']
        env = {}
        with captured_output() as out:
            lipi.run_lipi_if_block(lines, 0, env)
        self.assertEqual(out.getvalue().strip(), "")

    def test_while_loop_runs_correct_iterations(self):
        lines = ['while count <= 3:', '    print count', '    count = count + 1', 'end']
        env = {"count": 1}
        with captured_output() as out:
            lipi.run_lipi_while_block(lines, 0, env)
        self.assertEqual(len(out.getvalue().strip().split('\n')), 3)

    def test_telugu_unicode_string_roundtrip(self):
        env = {}
        lipi.run_lipi_line('స్వాగతం = "తెలుగు"', env)
        result = lipi.eval_lipi_expr('స్వాగతం', env)
        self.assertEqual(result, "తెలుగు")

    def test_comment_lines_ignored(self):
        env = {}
        lipi.run_lipi_line('# this is a comment', env)
        self.assertEqual(len(env), 0)

    def test_empty_line_is_safe(self):
        env = {}
        lipi.run_lipi_line('', env)
        lipi.run_lipi_line('   ', env)
        self.assertEqual(len(env), 0)

    def test_undefined_variable_raises(self):
        with self.assertRaises(Exception):
            lipi.eval_lipi_expr('undefined_var', {})

    def test_hello_example_file_runs(self):
        example = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', 'examples', 'hello.lipi.py'
        )
        with captured_output() as out:
            lipi.run_lipi_file(example)
        self.assertIn("నమస్తే", out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
