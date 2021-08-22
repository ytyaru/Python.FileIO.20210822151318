#!/usr/bin/env python3
# coding: utf8
import os,sys,pathlib,inspect
sys.path.append(str(pathlib.Path(__file__, '../../src').resolve()))
from file import FileObject
import unittest
from unittest.mock import MagicMock, patch, mock_open
class TestFileObject(unittest.TestCase):
    def test_init(self):
        for case in [
            '',
            'a',
            'a.txt',
            './a.txt',
            '../a.txt',
            '/tmp/a.txt',
            '/tmp/a.txt/',
        ]:
            with self.subTest(case=case):
                f = FileObject(case)
                self.assertEqual(f.Path, case)
    def test_path_set(self):
        expected = '/tmp/answer.txt'
        for case in [
            '',
            'a',
            'a.txt',
            './a.txt',
            '../a.txt',
            '/tmp/a.txt',
            '/tmp/a.txt/',
        ]:
            with self.subTest(case=case):
                f = FileObject(case)
                self.assertEqual(f.Path, case)
                f.Path = expected
                self.assertEqual(f.Path, expected)
    def test_encoding_get(self):
        f = FileObject('a.txt')
        self.assertEqual(f.Encoding, 'utf-8')
    def test_encoding_set(self):
        expected = 'shift-jis'
        f = FileObject('a.txt')
        f.Encoding = expected
        self.assertEqual(f.Encoding, expected)
    @patch('os.path.exists', return_value=False)
    def test_exists(self, mock_lib):
        actual = FileObject('a.txt').Exist
        mock_lib.assert_called_once()
        self.assertEqual(actual, mock_lib.return_value)

if __name__ == "__main__":
    unittest.main()
