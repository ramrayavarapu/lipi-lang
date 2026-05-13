#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import tempfile
import textwrap
import unittest


SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")


class TestCompatLazyImport(unittest.TestCase):
    def _run_python(self, script: str):
        return subprocess.run(
            [sys.executable, "-c", script],
            text=True,
            capture_output=True,
        )

    def test_import_lipi_does_not_require_lipi_v2(self):
        script = textwrap.dedent(
            f"""
            import builtins
            import sys

            sys.path.insert(0, {SRC_DIR!r})
            _orig_import = builtins.__import__

            def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
                if name == "lipi_v2" or name.startswith("lipi_v2."):
                    raise ImportError("blocked lipi_v2 import")
                return _orig_import(name, globals, locals, fromlist, level)

            builtins.__import__ = _guarded_import
            import lipi
            print("import-ok")
            """
        )

        proc = self._run_python(script)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("import-ok", proc.stdout)

    def test_run_lipi_file_compat_mode_without_lipi_v2(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".lipi.py", delete=False, encoding="utf-8") as handle:
            handle.write('print "Compat Lazy Import"\n')
            path = handle.name

        self.addCleanup(lambda: os.path.exists(path) and os.unlink(path))

        script = textwrap.dedent(
            f"""
            import builtins
            import sys

            sys.path.insert(0, {SRC_DIR!r})
            _orig_import = builtins.__import__

            def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
                if name == "lipi_v2" or name.startswith("lipi_v2."):
                    raise ImportError("blocked lipi_v2 import")
                return _orig_import(name, globals, locals, fromlist, level)

            builtins.__import__ = _guarded_import
            import lipi
            lipi.run_lipi_file({path!r}, mode="compat", lang="en")
            """
        )

        proc = self._run_python(script)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("Compat Lazy Import", proc.stdout)


if __name__ == "__main__":
    unittest.main()
