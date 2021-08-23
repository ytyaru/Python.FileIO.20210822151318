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
        mock_lib.assert_any_call(*(f.Path,), **{'mode':'r', 'encoding':f.Encoding})
        mock_lib.assert_any_call(*(f.Path,), **{'mode':'w', 'encoding':f.Encoding})

    def test_read_file(self):
        content = 'abc\n\ndef\n'
        p = pathlib.Path('/tmp/a.txt')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        f = LineTextFile(p)
        self.assertEqual(f.read(), content.split('\n')[:-1])
        self.assertEqual(f.read(), ['abc','','def'])
    def test_write_file(self):
        content = 'abc\n\ndef\n'
        p = pathlib.Path('/tmp/a.txt')
        f = LineTextFile(p)
        f.write(content.split('\n'))
        self.assertEqual(f.read(), content.split('\n')[:-1])
        self.assertEqual(f.read(), ['abc','','def'])
    def test_write_file_over_write(self):
        content = 'abc\n\ndef\n'
        p = pathlib.Path('/tmp/a.txt')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        f = LineTextFile(p)
        content_2 = 'ghi\njkl\n'
        f.write(content_2.split('\n'))
        self.assertEqual(f.read(), content_2.split('\n')[:-1])
        self.assertEqual(f.read(), ['ghi','jkl'])
    def test_append_file(self):
        content = 'abc\n\ndef\n'
        p = pathlib.Path('/tmp/a.txt')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        content_2 = 'ghi\njkl\n'
        f = LineTextFile(p)
        f.append(content_2.split('\n'))
        expected = content.split('\n')[:-1]
        expected.extend(content_2.split('\n')[:-1])
        self.assertEqual(f.read(), expected)
        self.assertEqual(f.read(), ['abc','','def','ghi','jkl'])
    def test_insert_file_0(self):
        content = 'abc\n\ndef\n'
        p = pathlib.Path('/tmp/a.txt')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        content_2 = 'ghi\njkl\n'
        f = LineTextFile(p)
        f.insert(content_2.split('\n')[:-1])
        expected = content_2.split('\n')[:-1]
        expected.extend(content.split('\n')[:-1])
        self.assertEqual(f.read(), expected)
        self.assertEqual(f.read(), ['ghi','jkl','abc','','def'])
    def test_insert_file_1(self):
        content = 'abc\n\ndef\n'
        p = pathlib.Path('/tmp/a.txt')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        content_2 = 'ghi\njkl\n'
        f = LineTextFile(p)
        pos = 1
        f.insert(content_2.split('\n')[:-1], pos)
        expected = content.split('\n')[:-1]
        expected[pos:pos] = content_2.split('\n')[:-1]
        self.assertEqual(f.read(), expected)
        self.assertEqual(f.read(), ['abc','ghi','jkl','','def'])
    def test_insert_file_last(self):
        content = 'abc\n\ndef\n'
        p = pathlib.Path('/tmp/a.txt')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        content_2 = 'ghi\njkl\n'
        f = LineTextFile(p)
        pos = len(content.split('\n')[:-1])
        f.insert(content_2.split('\n')[:-1], pos)
        expected = content.split('\n')[:-1]
        expected[pos:pos] = content_2.split('\n')[:-1]
        self.assertEqual(f.read(), expected)
        self.assertEqual(f.read(), ['abc','','def','ghi','jkl'])

if __name__ == "__main__":
    unittest.main()
