#!/usr/bin/env python
"""Tests for the core module."""

import unittest

from .core import format_fully_qualified_type_name, format_command_script_add

TEST_PACKAGE = f'{__package__}.core_test'
TEST_COMMAND = 'testCommand'
TEST_HELP = 'Help for testCommand'


class _TestClass:
    class Inner:
        pass


def _test_function():
    pass


TEST_CLASS = f'{TEST_PACKAGE}._TestClass'
TEST_FUNCTION = f'{TEST_PACKAGE}._test_function'


class CoreTest(unittest.TestCase):
    def test_format_fully_qualified_type_name(self):
        self.assertEqual(f'{TEST_CLASS}',
                         format_fully_qualified_type_name(_TestClass))
        self.assertEqual(f'{TEST_CLASS}.Inner',
                         format_fully_qualified_type_name(_TestClass.Inner))
        self.assertEqual('int', format_fully_qualified_type_name(int))

    def test_format_command_script_add(self):
        self.assertEqual(
            f'command script add -f {TEST_FUNCTION} {TEST_COMMAND}',
            format_command_script_add(TEST_COMMAND, _test_function))
        self.assertEqual(
            f'command script add -f {TEST_FUNCTION} ' +
            f"-h '{TEST_HELP}' {TEST_COMMAND}",
            format_command_script_add(TEST_COMMAND, _test_function, TEST_HELP))
        self.assertEqual(
            f'command script add -f {TEST_FUNCTION} ' +
            f"-h '{TEST_HELP}' -s synchronous {TEST_COMMAND}",
            format_command_script_add(TEST_COMMAND, _test_function, TEST_HELP,
                                      'synchronous'))
        self.assertEqual(
            f'command script add -f {TEST_FUNCTION} ' +
            f'-s asynchronous {TEST_COMMAND}',
            format_command_script_add(TEST_COMMAND,
                                      _test_function,
                                      synchronicity='asynchronous'))
        self.assertEqual(f'command script add -c {TEST_CLASS} {TEST_COMMAND}',
                         format_command_script_add(TEST_COMMAND, _TestClass))
        self.assertEqual(
            f'command script add -c {TEST_CLASS}.Inner ' +
            f'-s current {TEST_COMMAND}',
            format_command_script_add(TEST_COMMAND,
                                      _TestClass.Inner,
                                      synchronicity='current'))


if __name__ == '__main__':
    unittest.main()
