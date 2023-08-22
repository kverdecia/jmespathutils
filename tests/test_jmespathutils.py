#!/usr/bin/env python

"""Tests for `jmespathutils` package."""
import unittest
from unittest.mock import patch
import xml.parsers.expat
import uuid

import cuid
import xmltodict


import jmespathutils


class TestJmespathutils(unittest.TestCase):
    def test_jmespath_function_xml_to_json(self):
        a = cuid.cuid()
        b = cuid.cuid()
        xml = f'<root><a>{a}</a><b>{b}</b></root>'
        result = jmespathutils.search('xml_to_json(`{}`)'.format(xml), {})
        self.assertEqual(result, {'root': {'a': a, 'b': b}})

    def test_jmespath_function_xml_to_json_parameter_is_null(self):
        with patch.object(xmltodict, 'parse') as mock_parse:
            result = jmespathutils.search('xml_to_json(null)', {})
            self.assertIsNone(result)
            mock_parse.assert_not_called()

    def test_jmespath_function_xml_to_json_empty(self):
        self.assertRaises(xml.parsers.expat.ExpatError, jmespathutils.search, 'xml_to_json(``)', {})

    def test_jmespath_function_xml_to_json_invalid(self):
        src = '<root><a>'
        self.assertRaises(xml.parsers.expat.ExpatError, jmespathutils.search, 'xml_to_json(`{}`)'.format(src), {})

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

    def test_function_index_to_coordinates(self):
        text = f'{cuid.cuid()}\n{cuid.cuid()}\n{cuid.cuid()}\n{cuid.cuid()}\n'
        self.assertEqual(jmespathutils.index_to_coordinates(text, 0), (1, 1))
        self.assertEqual(jmespathutils.index_to_coordinates(text, 35), (2, 10))
