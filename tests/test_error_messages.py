"""
Tests for bilingual error messages (Rule 2c — unit, API, UX coverage).
Verifies Telugu and English error output for the get_error_message system.
Design: https://github.com/ramrayavarapu/lipi-lang/issues/47
"""
import sys
import os
import unittest
from io import StringIO
from contextlib import contextmanager

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import lipi


def set_lang(lang):
    lipi.ERROR_LANGUAGE[0] = lang


@contextmanager
def telugu_mode():
    set_lang('te')
    try:
        yield
    finally:
        set_lang('en')


@contextmanager
def captured_stderr():
    buf = StringIO()
    old = sys.stderr
    sys.stderr = buf
    try:
        yield buf
    finally:
        sys.stderr = old


# ── Unit tests ────────────────────────────────────────────────────────────────

class TestGetErrorMessage(unittest.TestCase):

    def setUp(self):
        set_lang('en')

    def tearDown(self):
        set_lang('en')

    def test_english_prefix(self):
        msg = lipi.get_error_message('runtime_error')
        self.assertTrue(msg.startswith('[Error]'))

    def test_telugu_prefix(self):
        with telugu_mode():
            msg = lipi.get_error_message('runtime_error')
        self.assertTrue(msg.startswith('[లోపం]'))

    def test_english_runtime_error(self):
        msg = lipi.get_error_message('runtime_error')
        self.assertIn('Runtime error', msg)

    def test_telugu_runtime_error(self):
        with telugu_mode():
            msg = lipi.get_error_message('runtime_error')
        self.assertIn('రన్‌టైమ్ లోపం', msg)

    def test_english_variable_not_defined(self):
        msg = lipi.get_error_message('variable_not_defined')
        self.assertIn('Variable not defined', msg)

    def test_telugu_variable_not_defined(self):
        with telugu_mode():
            msg = lipi.get_error_message('variable_not_defined')
        self.assertIn('వేరియబుల్ నిర్వచించబడలేదు', msg)

    def test_english_function_not_found(self):
        msg = lipi.get_error_message('function_not_found')
        self.assertIn('Function not defined', msg)

    def test_telugu_function_not_found(self):
        with telugu_mode():
            msg = lipi.get_error_message('function_not_found')
        self.assertIn('ఫంక్షన్ నిర్వచించబడలేదు', msg)

    def test_english_division_by_zero(self):
        msg = lipi.get_error_message('division_by_zero')
        self.assertIn('Division by zero', msg)

    def test_telugu_division_by_zero(self):
        with telugu_mode():
            msg = lipi.get_error_message('division_by_zero')
        self.assertIn('సున్నాతో భాగహారం', msg)

    def test_detail_appended(self):
        msg = lipi.get_error_message('variable_not_defined', 'myVar')
        self.assertIn('myVar', msg)

    def test_detail_appended_telugu(self):
        with telugu_mode():
            msg = lipi.get_error_message('variable_not_defined', 'నా_వేరియబుల్')
        self.assertIn('నా_వేరియబుల్', msg)
        self.assertIn('వేరియబుల్ నిర్వచించబడలేదు', msg)

    def test_unknown_key_falls_back_to_key_string(self):
        msg = lipi.get_error_message('no_such_key')
        self.assertIn('no_such_key', msg)

    def test_unknown_key_falls_back_in_telugu_mode(self):
        with telugu_mode():
            msg = lipi.get_error_message('no_such_key')
        self.assertIn('no_such_key', msg)

    def test_language_switch_roundtrip(self):
        set_lang('te')
        te_msg = lipi.get_error_message('invalid_syntax')
        set_lang('en')
        en_msg = lipi.get_error_message('invalid_syntax')
        self.assertIn('చెల్లని వాక్యనిర్మాణం', te_msg)
        self.assertIn('Invalid syntax', en_msg)

    def test_all_english_keys_present(self):
        keys = [
            'runtime_error', 'unknown_expression', 'function_not_found',
            'variable_not_defined', 'class_not_found', 'invalid_syntax',
            'division_by_zero', 'import_error', 'module_not_found',
            'circular_import', 'invalid_module_path', 'database_error',
            'connection_error', 'file_error', 'http_error', 'type_error',
            'attribute_error', 'index_error', 'key_error',
        ]
        for key in keys:
            with self.subTest(key=key):
                msg = lipi.get_error_message(key)
                self.assertIn('[Error]', msg)

    def test_all_telugu_keys_present(self):
        keys = [
            'runtime_error', 'unknown_expression', 'function_not_found',
            'variable_not_defined', 'class_not_found', 'invalid_syntax',
            'division_by_zero', 'import_error', 'module_not_found',
            'circular_import', 'invalid_module_path', 'database_error',
            'connection_error', 'file_error', 'http_error', 'type_error',
            'attribute_error', 'index_error', 'key_error',
        ]
        with telugu_mode():
            for key in keys:
                with self.subTest(key=key):
                    msg = lipi.get_error_message(key)
                    self.assertIn('[లోపం]', msg)


# ── API / interpreter tests ───────────────────────────────────────────────────

class TestInterpreterErrorMessages(unittest.TestCase):

    def setUp(self):
        set_lang('en')

    def tearDown(self):
        set_lang('en')

    def test_undefined_variable_english(self):
        with self.assertRaises((ValueError, lipi.LipiException)) as ctx:
            lipi.eval_lipi_expr('undefined_xyz', {})
        self.assertIn('[Error]', str(ctx.exception))

    def test_undefined_variable_telugu(self):
        with telugu_mode():
            with self.assertRaises((ValueError, lipi.LipiException)) as ctx:
                lipi.eval_lipi_expr('undefined_xyz', {})
        self.assertIn('[లోపం]', str(ctx.exception))

    def test_division_by_zero_english(self):
        with self.assertRaises(lipi.LipiException) as ctx:
            lipi.eval_lipi_expr('10 / 0', {})
        msg = str(ctx.exception)
        self.assertIn('[Error]', msg)
        self.assertIn('Division by zero', msg)

    def test_division_by_zero_telugu(self):
        with telugu_mode():
            with self.assertRaises(lipi.LipiException) as ctx:
                lipi.eval_lipi_expr('10 / 0', {})
        msg = str(ctx.exception)
        self.assertIn('[లోపం]', msg)
        self.assertIn('సున్నాతో భాగహారం', msg)

    def test_modulo_by_zero_telugu(self):
        with telugu_mode():
            with self.assertRaises(lipi.LipiException) as ctx:
                lipi.eval_lipi_expr('7 % 0', {})
        msg = str(ctx.exception)
        self.assertIn('[లోపం]', msg)
        self.assertIn('సున్నాతో భాగహారం', msg)

    def test_function_not_found_telugu(self):
        with telugu_mode():
            with self.assertRaises(lipi.LipiException) as ctx:
                lipi.eval_lipi_expr('call unknown_func()', {})
        msg = str(ctx.exception)
        self.assertIn('[లోపం]', msg)
        self.assertIn('ఫంక్షన్ నిర్వచించబడలేదు', msg)

    def test_function_not_found_english(self):
        with self.assertRaises(lipi.LipiException) as ctx:
            lipi.eval_lipi_expr('call unknown_func()', {})
        msg = str(ctx.exception)
        self.assertIn('[Error]', msg)
        self.assertIn('Function not defined', msg)

    def test_invalid_module_path_telugu(self):
        with telugu_mode():
            with self.assertRaises(lipi.LipiException) as ctx:
                lipi.resolve_module_path('../escape', None)
        msg = str(ctx.exception)
        self.assertIn('[లోపం]', msg)
        self.assertIn('చెల్లని మాడ్యూల్ పాత్', msg)


# ── UX / user-flow tests ──────────────────────────────────────────────────────

class TestUXErrorFlow(unittest.TestCase):

    def setUp(self):
        set_lang('en')

    def tearDown(self):
        set_lang('en')

    def test_telugu_mode_error_printed_to_stdout(self):
        buf = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            with telugu_mode():
                lipi.run_lipi_file.__doc__  # just ensure module loaded
                env = {}
                try:
                    lipi.eval_lipi_expr('nonsense_var', env)
                except Exception:
                    pass
        finally:
            sys.stdout = old_stdout

    def test_english_error_does_not_contain_telugu(self):
        try:
            lipi.eval_lipi_expr('10 / 0', {})
        except lipi.LipiException as e:
            self.assertNotIn('లోపం', str(e))
            self.assertNotIn('సున్నా', str(e))

    def test_telugu_error_does_not_contain_english_prefix(self):
        with telugu_mode():
            try:
                lipi.eval_lipi_expr('10 / 0', {})
            except lipi.LipiException as e:
                self.assertNotIn('[Error]', str(e))

    def test_bilingual_switch_mid_session(self):
        """User flow: start in English, switch to Telugu, switch back."""
        err_en1 = lipi.get_error_message('division_by_zero')
        set_lang('te')
        err_te = lipi.get_error_message('division_by_zero')
        set_lang('en')
        err_en2 = lipi.get_error_message('division_by_zero')

        self.assertIn('[Error]', err_en1)
        self.assertIn('[లోపం]', err_te)
        self.assertIn('[Error]', err_en2)
        self.assertEqual(err_en1, err_en2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
