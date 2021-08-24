#!/usr/bin/env python3
# coding: utf8
import os,sys,pathlib,inspect
sys.path.append(str(pathlib.Path(__file__, '../../src').resolve()))
from file import DsvFile
import unittest
from unittest.mock import MagicMock, patch, mock_open
class TestDsvFile(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError, msg="__init__() missing 2 required positional arguments: 'path' and 'delimiter'"):
            f = DsvFile()
        with self.assertRaises(TypeError, msg="__init__() missing 1 required positional argument: 'delimiter'"):
            f = DsvFile('')
    def test_Delimiter_get(self):
        for d in [',', '\t', '|', ';']:
            with self.subTest(case=d):
                f = DsvFile('a.txt', d)
                self.assertEqual(f.Delimiter, d)

    def test_read_0(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('')
        f = DsvFile(p, '	')
        actual = f.read()
        self.assertEqual(list(actual), [])
    def test_read_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10''')
        f = DsvFile(p, '	')
        actual = f.read()
        self.assertEqual(list(actual), [['Yamada','10']])
    def test_read_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10
Suzuki	22''')
        f = DsvFile(p, '	')
        actual = f.read()
        self.assertEqual(list(actual), [['Yamada','10'],['Suzuki','22']])
    def test_read_last_newline(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10
Suzuki	22
''')
        f = DsvFile(p, '	')
        actual = f.read()
        self.assertEqual(list(actual), [['Yamada','10'],['Suzuki','22']])
    def test_read_in_blank(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''
Yamada	10

Suzuki	22

''')
        f = DsvFile(p, '	')
        actual = f.read()
        self.assertEqual(list(actual), [[],['Yamada','10'],[],['Suzuki','22'],[]])
    def test_read_in_comment(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''# not comment out
Yamada	10''')
        f = DsvFile(p, '	')
        actual = f.read()
        self.assertEqual(list(actual), [['# not comment out'],['Yamada','10']])
    def test_read_has_not_names_and_types(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	')
        actual = f.read()
        self.assertEqual(f.Names, [])
        self.assertEqual(f.Types, [])
        self.assertEqual(list(actual), [['Yamada','10'],['Suzuki','22'],['Tanaka','35']])
    def test_read_has_names(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read()
        expected = [
            f.RowType('Yamada','10'),
            f.RowType('Suzuki','22'),
            f.RowType('Tanaka','35'),
        ]
        self.assertEqual(f.Names, ['name', 'age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(list(actual), expected)
    def test_read_has_names_and_types(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read()
        expected = [
            f.RowType('Yamada',10),
            f.RowType('Suzuki',22),
            f.RowType('Tanaka',35),
        ]
        self.assertEqual(f.Names, ['name', 'age'])
        self.assertEqual(f.Types, ['str', 'int'])
        self.assertEqual(list(actual), expected)
        self.assertEqual(type(list(actual)[0].name), str)
        self.assertEqual(type(list(actual)[0].age), int)

    def test_read_to_dictlist_has_not_name(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10''')
        f = DsvFile(p, '	')
        with self.assertRaises(ValueError, msg='header_line_numが1より小さいです。1以上にしてください。'):
            actual = f.read_to_dictlist()
    def test_read_to_dictlist_0(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_dictlist()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(list(actual), [])
    def test_read_to_dictlist_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_dictlist()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(list(actual), [{'name': 'Yamada', 'age': '10'}])
    def test_read_to_dictlist_1_typed(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_dictlist()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(list(actual), [{'name': 'Yamada', 'age': 10}])





if __name__ == "__main__":
    unittest.main()
