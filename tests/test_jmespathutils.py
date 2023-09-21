#!/usr/bin/env python

"""Tests for `jmespathutils` package."""
import unittest
from unittest.mock import patch
import xml.parsers.expat
import uuid

import cuid
import xmltodict


import jmespath.exceptions
import jmespathutils


class TestJmespathutils(unittest.TestCase):
    def test_jmespath_function_xml_to_json(self):
        a = cuid.cuid()
        b = cuid.cuid()
        xml = f'<root><a>{a}</a><b>{b}</b></root>'
        result = jmespathutils.search('xml_to_json(@)', xml)
        self.assertEqual(result, {'root': {'a': a, 'b': b}})

    def test_jmespath_function_xml_to_json_parameter_is_null(self):
        with patch.object(xmltodict, 'parse') as mock_parse:
            result = jmespathutils.search('xml_to_json(@)', None)
            self.assertIsNone(result)
            mock_parse.assert_not_called()

    def test_jmespath_function_xml_to_json_empty(self):
        self.assertRaises(xml.parsers.expat.ExpatError, jmespathutils.search, 'xml_to_json(@)', '')

    def test_jmespath_function_xml_to_json_invalid(self):
        src = '<root><a>'
        self.assertRaises(xml.parsers.expat.ExpatError, jmespathutils.search, 'xml_to_json(@)', src)

    def test_jmespath_function_uuid(self):
        expected = str(uuid.uuid4())
        with patch.object(uuid, 'uuid4', return_value=expected):
            result = jmespathutils.search('uuid()', {})
            self.assertEqual(result, expected)

    def test_jmespath_function_cuid(self):
        expected = str(cuid.cuid())
        with patch.object(cuid, 'cuid', return_value=expected):
            result = jmespathutils.search('cuid()', {})
            self.assertEqual(result, expected)

    def test_jmespath_function_unique(self):
        result = jmespathutils.search('unique(@)', [1, 2, 3, 1, 2, 3, 1, 2, 3])
        self.assertEqual(result, [1, 2, 3])

    def test_jmespath_function_unique_by(self):
        result = jmespathutils.search('unique_by(@, &a)', [{'a': 1}, {'a': 2}, {'a': 1}, {'a': 2}])
        self.assertEqual(result, [{'a': 1}, {'a': 2}])

    def test_jmespath_function_to_object(self):
        result = jmespathutils.search("to_object(@, 'a')", [1, 2, 3])
        self.assertEqual(result, [{'a': 1}, {'a': 2}, {'a': 3}])

    def test_function_index_to_coordinates(self):
        text = f'{cuid.cuid()}\n{cuid.cuid()}\n{cuid.cuid()}\n{cuid.cuid()}\n'
        self.assertEqual(jmespathutils.index_to_coordinates(text, 0), (1, 1))
        self.assertEqual(jmespathutils.index_to_coordinates(text, 35), (2, 10))

    def test_context_function_initialized(self):
        data = {cuid.cuid(): cuid.cuid()}
        functions = jmespathutils.functions.ContextFunctions(data)
        self.assertEqual(functions._context, data)
        self.assertEqual(functions._func_context(), data)

    def test_jmespath_function_context_not_initialized(self):
        with self.assertRaises(jmespath.exceptions.UnknownFunctionError, msg='Unknown function: context()'):
            self.assertIsNone(jmespathutils.search('context()', {}))

    def test_jmespath_function_context_initialized(self):
        data = {cuid.cuid(): cuid.cuid()}
        result = jmespathutils.search('context()', {}, context_function_data=data)
        self.assertEqual(result, data)
