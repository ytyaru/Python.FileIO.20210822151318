#!/usr/bin/env python3
# coding: utf8
import os,sys,pathlib,inspect
sys.path.append(str(pathlib.Path(__file__, '../../src').resolve()))
from file import TextFile
import unittest
from unittest.mock import MagicMock, patch, mock_open
class TestTextFile(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError, msg="__init__() missing 1 required positional argument: 'path'"):
            f = TextFile()
    @patch('builtins.open')
    def test_read(self, mock_lib):
        f = TextFile('a.txt')
        f.read()
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'r', 'encoding':f.Encoding})
    @patch('builtins.open')
    def test_write(self, mock_lib):
        f = TextFile('a.txt')
        f.write('')
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'w', 'encoding':f.Encoding})
    @patch('builtins.open')
    def test_append(self, mock_lib):
        f = TextFile('a.txt')
        f.append('')
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'a', 'encoding':f.Encoding})

if __name__ == "__main__":
    unittest.main()
