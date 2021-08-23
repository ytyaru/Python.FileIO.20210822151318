#!/usr/bin/env python3
# coding: utf8
import os,sys,pathlib,inspect
sys.path.append(str(pathlib.Path(__file__, '../../src').resolve()))
from file import LineTextFile
import unittest
from unittest.mock import MagicMock, patch, mock_open
class TestLineTextFile(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError, msg="__init__() missing 1 required positional argument: 'path'"):
            f = LineTextFile()
    @patch('builtins.open')
    def test_read(self, mock_lib):
        f = LineTextFile('a.txt')
        f.read()
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'r', 'encoding':f.Encoding})
#        mock_lib.assert_called_once()
#        with self.assertRaises(TypeError, msg="Can't instantiate abstract class File with abstract methods read, write"):
    @patch('builtins.open')
    def test_write(self, mock_lib):
        f = LineTextFile('a.txt')
        f.write('')
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'w', 'encoding':f.Encoding})
    @patch('builtins.open')
    def test_append(self, mock_lib):
        f = LineTextFile('a.txt')
        f.append('')
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'a', 'encoding':f.Encoding})
    @patch('builtins.open')
    def test_insert(self, mock_lib):
        f = LineTextFile('a.txt')
        f.insert('')
#        mock_lib.assert_called_with(*(f.Path,), **{'mode':'r', 'encoding':f.Encoding})
#        mock_lib.assert_called_with(*(f.Path,), **{'mode':'w', 'encoding':f.Encoding})
        mock_lib.assert_any_call(*(f.Path,), **{'mode':'r', 'encoding':f.Encoding})
        mock_lib.assert_any_call(*(f.Path,), **{'mode':'w', 'encoding':f.Encoding})
    """
    @patch('builtins.open')
    def test_read(self, mock_lib):
        mock_lib.return_value=['content']
        f = LineTextFile('a.txt')
        actual = f.read()
        mock_lib.assert_any_call(*(f.Path,), **{'mode':'r', 'encoding':f.Encoding})
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'r', 'encoding':f.Encoding})
        mock_lib.assertEqual(actual, ['content'])
    """


if __name__ == "__main__":
    unittest.main()
