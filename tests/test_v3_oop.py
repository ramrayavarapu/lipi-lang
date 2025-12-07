#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Lipi v3.0 Object-Oriented Programming
Tests classes, inheritance, method overriding, and instance variables
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.lipi import runtime, execute_block, LipiClassInstance


class TestOOP(unittest.TestCase):
    """Test v3.0 OOP features"""

    def setUp(self):
        """Set up test environment"""
        # Clear runtime state
        runtime.functions.clear()
        runtime.classes.clear()

    def test_class_definition(self):
        """Test basic class definition"""
        code = [
            'క్లాస్ Person:',
            '    పనిచేయి __init__(స్వీయ, name):',
            '        స్వీయ.name = name',
            '    ముగింపు',
            'ముగింపు'
        ]

        env = {}
        execute_block(code, env)

        # Check class was created
        self.assertIn('Person', runtime.classes)
        self.assertIn('__init__', runtime.classes['Person']['methods'])

    def test_object_instantiation(self):
        """Test creating objects"""
        code = [
            'class Box:',
            '    function __init__(self, label):',
            '        self.label = label',
            '    end',
            'end',
            'box = Box("Test")'
        ]

        env = {}
        execute_block(code, env)

        # Check object created
        self.assertIn('box', env)
        self.assertIsInstance(env['box'], LipiClassInstance)
        self.assertEqual(env['box'].attributes['label'], "Test")

    def test_method_calls(self):
        """Test calling methods"""
        code = [
            'class Calculator:',
            '    function __init__(self, value):',
            '        self.value = value',
            '    end',
            '    function double(self):',
            '        return self.value + self.value',
            '    end',
            'end',
            'calc = Calculator("5")',
            'result = call calc.double()'
        ]

        env = {}
        execute_block(code, env)

        self.assertEqual(env['result'], "55")  # String concatenation

    def test_instance_attributes(self):
        """Test instance attributes"""
        code = [
            'క్లాస్ Counter:',
            '    పనిచేయి __init__(స్వీయ):',
            '        స్వీయ.count = "0"',
            '    ముగింపు',
            '    పనిచేయి increment(స్వీయ):',
            '        స్వీయ.count = స్వీయ.count + "1"',
            '    ముగింపు',
            'ముగింపు',
            'c = Counter()',
            'కాల్ c.increment()',
            'కాల్ c.increment()',
            'value = c.count'
        ]

        env = {}
        execute_block(code, env)

        self.assertEqual(env['value'], "011")

    def test_simple_inheritance(self):
        """Test basic inheritance"""
        code = [
            'class Animal:',
            '    function __init__(self, name):',
            '        self.name = name',
            '    end',
            '    function speak(self):',
            '        return "Animal sound"',
            '    end',
            'end',
            'class Dog(Animal):',
            '    function speak(self):',
            '        return "Bark"',
            '    end',
            'end',
            'dog = Dog("Buddy")',
            'sound = call dog.speak()'
        ]

        env = {}
        execute_block(code, env)

        # Check inheritance
        self.assertEqual(env['dog'].attributes['name'], "Buddy")
        self.assertEqual(env['sound'], "Bark")  # Overridden method

    def test_parent_method_access(self):
        """Test accessing parent methods"""
        code = [
            'క్లాస్ Vehicle:',
            '    పనిచేయి __init__(స్వీయ, brand):',
            '        స్వీయ.brand = brand',
            '    ముగింపు',
            '    పనిచేయి info(స్వీయ):',
            '        రిటర్న్ "Vehicle: " + స్వీయ.brand',
            '    ముగింపు',
            'ముగింపు',
            'క్లాస్ Car(Vehicle):',
            '    పనిచేయి honk(స్వీయ):',
            '        రిటర్న్ "Beep"',
            '    ముగింపు',
            'ముగింపు',
            'car = Car("Toyota")',
            'result = కాల్ car.info()'
        ]

        env = {}
        execute_block(code, env)

        # Check parent method works
        self.assertEqual(env['result'], "Vehicle: Toyota")

    def test_multi_level_inheritance(self):
        """Test multi-level inheritance"""
        code = [
            'class A:',
            '    function method_a(self):',
            '        return "A"',
            '    end',
            'end',
            'class B(A):',
            '    function method_b(self):',
            '        return "B"',
            '    end',
            'end',
            'class C(B):',
            '    function method_c(self):',
            '        return "C"',
            '    end',
            'end',
            'obj = C()',
            'ra = call obj.method_a()',
            'rb = call obj.method_b()',
            'rc = call obj.method_c()'
        ]

        env = {}
        execute_block(code, env)

        # All three methods should work
        self.assertEqual(env['ra'], "A")
        self.assertEqual(env['rb'], "B")
        self.assertEqual(env['rc'], "C")

    def test_method_overriding(self):
        """Test method overriding in inheritance"""
        code = [
            'class Base:',
            '    function greet(self):',
            '        return "Base"',
            '    end',
            'end',
            'class Derived(Base):',
            '    function greet(self):',
            '        return "Derived"',
            '    end',
            'end',
            'base = Base()',
            'derived = Derived()',
            'r1 = call base.greet()',
            'r2 = call derived.greet()'
        ]

        env = {}
        execute_block(code, env)

        self.assertEqual(env['r1'], "Base")
        self.assertEqual(env['r2'], "Derived")

    def test_constructor_inheritance(self):
        """Test that child uses parent constructor if not defined"""
        code = [
            'క్లాస్ Parent:',
            '    పనిచేయి __init__(స్వీయ, value):',
            '        స్వీయ.value = value',
            '    ముగింపు',
            'ముగింపు',
            'క్లాస్ Child(Parent):',
            '    పనిచేయి extra(స్వీయ):',
            '        రిటర్న్ "extra"',
            '    ముగింపు',
            'ముగింపు',
            'child = Child("test")',
            'val = child.value'
        ]

        env = {}
        execute_block(code, env)

        # Child should have parent's attribute
        self.assertEqual(env['val'], "test")

    def test_bilingual_oop(self):
        """Test mixing Telugu and English in OOP"""
        code = [
            'class EnglishClass:',
            '    function english_method(self):',
            '        return "English"',
            '    end',
            'end',
            'క్లాస్ TeluguClass(EnglishClass):',
            '    పనిచేయి telugu_method(స్వీయ):',
            '        రిటర్న్ "Telugu"',
            '    ముగింపు',
            'ముగింపు',
            'obj = TeluguClass()',
            'r1 = call obj.english_method()',
            'r2 = కాల్ obj.telugu_method()'
        ]

        env = {}
        execute_block(code, env)

        self.assertEqual(env['r1'], "English")
        self.assertEqual(env['r2'], "Telugu")


if __name__ == '__main__':
    unittest.main()
