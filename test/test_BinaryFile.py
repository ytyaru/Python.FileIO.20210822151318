#!/usr/bin/env python3
# coding: utf8
import os,sys,pathlib,inspect
sys.path.append(str(pathlib.Path(__file__, '../../src').resolve()))
from file import BinaryFile
import unittest
from unittest.mock import MagicMock, patch, mock_open
class TestBinaryFile(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError, msg="__init__() missing 1 required positional argument: 'path'"):
            f = BinaryFile()
    @patch('builtins.open')
    def test_read(self, mock_lib):
        f = BinaryFile('a.txt')
        f.read()
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'rb'})
    @patch('builtins.open')
    def test_write(self, mock_lib):
        f = BinaryFile('a.txt')
        f.write(b'')
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'wb'})
    @patch('builtins.open')
    def test_over_write(self, mock_lib):
        f = BinaryFile('a.txt')
        f.over_write(b'')
        mock_lib.assert_called_once_with(*(f.Path,), **{'mode':'r+'})

if __name__ == "__main__":
    unittest.main()
