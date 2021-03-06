#!/usr/bin/env python
"""Tests for the core module."""

import unittest

import lldb

from lldb_script_utils import debugger_utils

TEST_PACKAGE = f'{__package__}.debugger_utils_test'
TEST_CLASS = f'{TEST_PACKAGE}._TestClass'
TEST_FUNCTION = f'{TEST_PACKAGE}._test_function'
TEST_SUMMARY_FUNCTION = f'{TEST_PACKAGE}._type_summary_function'
TEST_COMMAND = 'testCommand'
TEST_HELP = 'Help for testCommand'
TEST_TYPES = ['int *', 'bool']
TEST_TYPE_NAMES = "'int *' bool"


class _TestClass:
    class Inner:
        pass


def _test_function():
    pass


def _type_summary_function(unused_: lldb.SBValue, _: dict) -> str:
    return ''


class _TestDebugger(lldb.SBDebugger):
    def __init__(self, *args):
        super().__init__(*args)
        self.handled_command = ''

    def HandleCommand(self, command):
        self.handled_command = command


class CoreTest(unittest.TestCase):
    def test_format_fully_qualified_type_name(self):
        self.assertEqual(
            f'{TEST_CLASS}',
            debugger_utils.format_fully_qualified_type_name(_TestClass))
        self.assertEqual(
            f'{TEST_CLASS}.Inner',
            debugger_utils.format_fully_qualified_type_name(_TestClass.Inner))
        self.assertEqual('int',
                         debugger_utils.format_fully_qualified_type_name(int))

    def test_format_command_script_add(self):
        debugger = _TestDebugger()
        debugger_utils.handle_command_script_add(debugger, TEST_COMMAND,
                                                 _test_function)
        self.assertEqual(
            f'command script add --function {TEST_FUNCTION} {TEST_COMMAND}',
            debugger.handled_command)
        debugger_utils.handle_command_script_add(debugger,
                                                 TEST_COMMAND,
                                                 _test_function,
                                                 help=TEST_HELP)
        self.assertEqual(
            f'command script add --function {TEST_FUNCTION} ' +
            f"--help '{TEST_HELP}' {TEST_COMMAND}", debugger.handled_command)
        debugger_utils.handle_command_script_add(debugger,
                                                 TEST_COMMAND,
                                                 _test_function,
                                                 help=TEST_HELP,
                                                 synchronicity='synchronous')
        self.assertEqual(
            f'command script add --function {TEST_FUNCTION} ' +
            f"--help '{TEST_HELP}' --synchronicity synchronous {TEST_COMMAND}",
            debugger.handled_command)
        debugger_utils.handle_command_script_add(debugger,
                                                 TEST_COMMAND,
                                                 _test_function,
                                                 synchronicity='asynchronous')
        self.assertEqual(
            f'command script add --function {TEST_FUNCTION} ' +
            f'--synchronicity asynchronous {TEST_COMMAND}',
            debugger.handled_command)
        debugger_utils.handle_command_script_add(debugger, TEST_COMMAND,
                                                 _TestClass)
        self.assertEqual(
            f'command script add --class {TEST_CLASS} {TEST_COMMAND}',
            debugger.handled_command)
        debugger_utils.handle_command_script_add(debugger,
                                                 TEST_COMMAND,
                                                 _TestClass.Inner,
                                                 synchronicity='current')
        self.assertEqual(
            f'command script add --class {TEST_CLASS}.Inner ' +
            f'--synchronicity current {TEST_COMMAND}',
            debugger.handled_command)

    def test_format_type_summary_add(self):
        debugger = _TestDebugger()
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               inline_children=True)
        self.assertEqual(
            'type summary add --inline-children ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               omit_names=True)
        self.assertEqual('type summary add --omit-names ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               expand=True)
        self.assertEqual('type summary add --expand ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               hide_empty=True)
        self.assertEqual('type summary add --hide-empty ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               skip_pointers=True)
        self.assertEqual('type summary add --skip-pointers ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               skip_references=True)
        self.assertEqual(
            'type summary add --skip-references ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               no_value=True)
        self.assertEqual('type summary add --no-value ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               regex=True)
        self.assertEqual('type summary add --regex ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               summary_string='short_summary')
        self.assertEqual(
            'type summary add --summary-string short_summary ' +
            TEST_TYPE_NAMES, debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               summary_string='long summary')
        self.assertEqual(
            "type summary add --summary-string 'long summary' " +
            TEST_TYPE_NAMES, debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               cascade=True)
        self.assertEqual('type summary add --cascade true ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               cascade=False)
        self.assertEqual('type summary add --cascade false ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_summary_add(
            debugger, *TEST_TYPES, python_function=_type_summary_function)
        self.assertEqual(
            f'type summary add --python-function {TEST_SUMMARY_FUNCTION} ' +
            TEST_TYPE_NAMES, debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               python_script='short_script')
        self.assertEqual(
            'type summary add --python-script short_script ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               python_script='long script')
        self.assertEqual(
            "type summary add --python-script 'long script' " +
            TEST_TYPE_NAMES, debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               category='short_category')
        self.assertEqual(
            'type summary add --category short_category ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               category='long category')
        self.assertEqual(
            "type summary add --category 'long category' " + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               name='short_name')
        self.assertEqual(
            'type summary add --name short_name ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_summary_add(debugger,
                                               *TEST_TYPES,
                                               name='long name')
        self.assertEqual(
            "type summary add --name 'long name' " + TEST_TYPE_NAMES,
            debugger.handled_command)

    def test_format_type_synthetic_add(self):
        debugger = _TestDebugger()
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 *TEST_TYPES,
                                                 skip_pointers=True)
        self.assertEqual(
            'type synthetic add --skip-pointers ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 *TEST_TYPES,
                                                 skip_references=True)
        self.assertEqual(
            'type synthetic add --skip-references ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 *TEST_TYPES,
                                                 regex=True)
        self.assertEqual('type synthetic add --regex ' + TEST_TYPE_NAMES,
                         debugger.handled_command)
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 *TEST_TYPES,
                                                 cascade=True)
        self.assertEqual(
            'type synthetic add --cascade true ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 *TEST_TYPES,
                                                 cascade=False)
        self.assertEqual(
            'type synthetic add --cascade false ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 *TEST_TYPES,
                                                 category='short_category')
        self.assertEqual(
            'type synthetic add --category short_category ' + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 *TEST_TYPES,
                                                 category='long category')
        self.assertEqual(
            "type synthetic add --category 'long category' " + TEST_TYPE_NAMES,
            debugger.handled_command)
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 *TEST_TYPES,
                                                 python_class=_TestClass)
        self.assertEqual(
            f'type synthetic add --python-class {TEST_CLASS} ' +
            TEST_TYPE_NAMES, debugger.handled_command)


if __name__ == '__main__':
    unittest.main()
