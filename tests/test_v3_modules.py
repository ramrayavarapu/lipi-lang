#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Lipi v3.0 Module System
Tests module import, export, caching, and circular dependency detection
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.lipi import runtime, execute_block, LipiException


class TestModuleSystem(unittest.TestCase):
    """Test v3.0 module import system"""

    def setUp(self):
        """Set up test environment"""
        # Clear runtime state
        runtime.functions.clear()
        runtime.classes.clear()
        runtime.loaded_modules.clear()
        runtime.module_stack.clear()
        runtime.exports.clear()

        # Create temporary directory for test modules
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_simple_import(self):
        """Test basic module import"""
        # Create a simple module
        module_file = os.path.join(self.test_dir, 'simple.lipi.py')
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write('పనిచేయి hello():\n')
            f.write('    రిటర్న్ "Hello from module"\n')
            f.write('ముగింపు\n')
            f.write('ఎగుమతి hello\n')

        # Create main file that imports
        main_file = os.path.join(self.test_dir, 'main.lipi.py')
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write('దిగుమతి hello from "simple"\n')
            f.write('result = కాల్ hello()\n')

        # Run main file
        runtime.current_module_path = main_file
        with open(main_file, 'r', encoding='utf-8') as f:
            lines = [ln.rstrip('\n') for ln in f]

        env = {}
        execute_block(lines, env)

        # Check result
        self.assertEqual(env['result'], "Hello from module")

    def test_module_caching(self):
        """Test that modules are loaded only once"""
        # Create a module with a counter
        module_file = os.path.join(self.test_dir, 'counter.lipi.py')
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write('count = "1"\n')
            f.write('ఎగుమతి count\n')

        # Import twice
        main_file = os.path.join(self.test_dir, 'main2.lipi.py')
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write('దిగుమతి count from "counter"\n')
            f.write('value1 = count\n')
            f.write('import count from "counter"\n')
            f.write('value2 = count\n')

        runtime.current_module_path = main_file
        with open(main_file, 'r', encoding='utf-8') as f:
            lines = [ln.rstrip('\n') for ln in f]

        env = {}
        execute_block(lines, env)

        # Both should be the same (module cached)
        self.assertEqual(env['value1'], "1")
        self.assertEqual(env['value2'], "1")

    def test_bilingual_import(self):
        """Test Telugu and English mixed imports"""
        # Create module with both Telugu and English
        module_file = os.path.join(self.test_dir, 'mixed.lipi.py')
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write('పనిచేయి telugu_func():\n')
            f.write('    రిటర్న్ "Telugu"\n')
            f.write('ముగింపు\n')
            f.write('function english_func():\n')
            f.write('    return "English"\n')
            f.write('end\n')
            f.write('export telugu_func, english_func\n')

        main_file = os.path.join(self.test_dir, 'main3.lipi.py')
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write('దిగుమతి telugu_func, english_func from "mixed"\n')
            f.write('r1 = కాల్ telugu_func()\n')
            f.write('r2 = call english_func()\n')

        runtime.current_module_path = main_file
        with open(main_file, 'r', encoding='utf-8') as f:
            lines = [ln.rstrip('\n') for ln in f]

        env = {}
        execute_block(lines, env)

        self.assertEqual(env['r1'], "Telugu")
        self.assertEqual(env['r2'], "English")

    def test_multiple_exports(self):
        """Test exporting multiple items"""
        module_file = os.path.join(self.test_dir, 'multi.lipi.py')
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write('value1 = "first"\n')
            f.write('value2 = "second"\n')
            f.write('value3 = "third"\n')
            f.write('ఎగుమతి value1, value2, value3\n')

        main_file = os.path.join(self.test_dir, 'main4.lipi.py')
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write('import value1, value2, value3 from "multi"\n')

        runtime.current_module_path = main_file
        with open(main_file, 'r', encoding='utf-8') as f:
            lines = [ln.rstrip('\n') for ln in f]

        env = {}
        execute_block(lines, env)

        self.assertEqual(env['value1'], "first")
        self.assertEqual(env['value2'], "second")
        self.assertEqual(env['value3'], "third")


if __name__ == '__main__':
    unittest.main()
