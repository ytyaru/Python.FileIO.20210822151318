#!/usr/bin/env python3
# coding: utf8
import os,sys,pathlib,inspect
from collections import namedtuple
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
    def test_read_header_only_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(list(actual), [])
    def test_read_header_only_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(list(actual), [])

    def test_read_to_dictlist_has_not_name(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10''')
        f = DsvFile(p, '	')
#        with self.assertRaisesRegex(ValueError, 'header_line_numが1より小さいです。1以上にしてください。'):
#            actual = f.read_to_dictlist()
        actual = f.read_to_dictlist()
        self.assertEqual(f.Names, [])
        self.assertEqual(f.Types, [])
        self.assertEqual(list(actual), [['Yamada', '10']])
    def test_read_to_dictlist_header_only_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_dictlist()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(list(actual), [])
    def test_read_to_dictlist_header_only_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_dictlist()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
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
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(list(actual), [{'name': 'Yamada', 'age': 10}])
    def test_read_to_dictlist_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10
Suzuki	22''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_dictlist()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(list(actual), [{'name': 'Yamada', 'age': '10'},{'name': 'Suzuki', 'age': '22'}])
    def test_read_to_dictlist_2_typed(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	22''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_dictlist()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(list(actual), [{'name': 'Yamada', 'age': 10},{'name': 'Suzuki', 'age': 22}])

    def test_read_to_namedtuple_has_not_name(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10''')
        f = DsvFile(p, '	')
#        with self.assertRaisesRegex(ValueError, 'header_line_numが1より小さいです。1以上にしてください。'):
#            actual = f.read_to_namedtuple()
        actual = f.read_to_namedtuple()
        self.assertEqual(f.Names, [])
        self.assertEqual(f.Types, [])
        self.assertEqual(list(actual), [['Yamada','10']])
    def test_read_to_namedtuple_header_only_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_namedtuple()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(list(actual), [])
    def test_read_to_namedtuple_header_only_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_namedtuple()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(list(actual), [])
    def test_read_to_namedtuple_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_namedtuple()
        expected = [f.RowType('Yamada','10')]
        self.assertTrue(all([hasattr(f.RowType, n) for n in f.Names]))
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(list(actual), expected)
    def test_read_to_namedtuple_1_typed(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_namedtuple()
        expected = [f.RowType('Yamada',10)]
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(list(actual), expected)
    def test_read_to_namedtuple_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10
Suzuki	22''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_namedtuple()
        expected = [
            f.RowType('Yamada','10'),
            f.RowType('Suzuki','22'),
        ]
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(list(actual), expected)
    def test_read_to_namedtuple_2_typed(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	22''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_namedtuple()
        expected = [
            f.RowType('Yamada',10),
            f.RowType('Suzuki',22),
        ]
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(list(actual), expected)

    def test_read_to_list_has_not_name(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10''')
        f = DsvFile(p, '	')
        actual = f.read_to_list()
        self.assertEqual(f.Names, [])
        self.assertEqual(f.Types, [])
        self.assertEqual(list(actual), [['Yamada','10']])
    def test_read_to_list_header_only_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_list()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(actual, [])
    def test_read_to_list_header_only_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_list()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str', 'int'])
        self.assertEqual(actual, [])
    def test_read_to_list_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_list()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(actual, [['Yamada', '10']])
    def test_read_to_list_1_typed(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_list()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(actual, [['Yamada', '10']])
    def test_read_to_list_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10
Suzuki	22''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.read_to_list()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(actual, [['Yamada', '10'],['Suzuki', '22']])
    def test_read_to_list_2_typed(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	22''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.read_to_list()
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(actual, [['Yamada', '10'],['Suzuki', '22']])

    def test_select_list_pos_1(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	')
        actual = f.select('Suzuki')
        self.assertEqual(f.Names, [])
        self.assertEqual(f.Types, [])
        self.assertEqual(actual, [['Suzuki', '22']])
    def test_select_list_pos_2(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	')
        actual = f.select(None, '22')
        self.assertEqual(f.Names, [])
        self.assertEqual(f.Types, [])
        self.assertEqual(actual, [['Suzuki', '22']])
    def test_select_typed_str(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.select(name='Suzuki')
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(actual, [f.RowType('Suzuki', 22)])
    def test_select_typed_int(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.select(age=22)
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(actual, [f.RowType('Suzuki', 22)])
    def test_select_named_callable_str(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.select(name=lambda x: 'Suzuki' == x)
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(actual, [f.RowType('Suzuki', '22')])
    def test_select_named_callable_int(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=1)
        actual = f.select(age=lambda x: '22' == x)
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, [])
        self.assertEqual(actual, [f.RowType('Suzuki', '22')])
    def test_select_typed_callable_str(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.select(name=lambda x: 'Suzuki' == x)
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(actual, [f.RowType('Suzuki', 22)])
    def test_select_typed_callable_int(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.select(age=lambda x: 22 <= x)
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(actual, [f.RowType('Suzuki', 22), f.RowType('Tanaka', 35)])
    def test_select_typed_callable_str_int(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10
Suzuki	3
Suzuki	22
Tanaka	35''')
        f = DsvFile(p, '	', header_line_num=2)
        actual = f.select(name='Suzuki', age=lambda x: 22 <= x)
        self.assertEqual(f.Names, ['name','age'])
        self.assertEqual(f.Types, ['str','int'])
        self.assertEqual(actual, [f.RowType('Suzuki', 22)])

    def test_write_from_list_type_error(self):
        p = pathlib.Path('/tmp/a.tsv')
        rows = []
        f = DsvFile(p, '	')
        with self.assertRaises(ValueError, msg='引数は二重配列にしてください。'):
            f.write(rows)
    def test_write_from_list_len_error(self):
        p = pathlib.Path('/tmp/a.tsv')
        rows = [[]]
        f = DsvFile(p, '	')
        with self.assertRaises(ValueError, msg='要素がありません。引数の配列に1つ以上要素を加えてください。'):
            f.write(rows)
    def test_write_from_named_type_error(self):
        p = pathlib.Path('/tmp/a.tsv')
        rows = []
        f = DsvFile(p, '	', 1)
        with self.assertRaises(ValueError, msg='引数は二重配列にしてください。'):
            f.write(rows)
    def test_write_from_named_len_error(self):
        p = pathlib.Path('/tmp/a.tsv')
        rows = [[]]
        f = DsvFile(p, '	', 1)
        with self.assertRaises(ValueError, msg='要素がありません。引数の配列に1つ以上要素を加えてください。'):
            f.write(rows)
    def test_write_from_typed_type_error(self):
        p = pathlib.Path('/tmp/a.tsv')
        rows = []
        f = DsvFile(p, '	', 2)
        with self.assertRaises(ValueError, msg='引数は二重配列にしてください。'):
            f.write(rows)
    def test_write_from_typed_len_error(self):
        p = pathlib.Path('/tmp/a.tsv')
        rows = [[]]
        f = DsvFile(p, '	', 2)
        with self.assertRaises(ValueError, msg='要素がありません。引数の配列に1つ以上要素を加えてください。'):
            f.write(rows)

    def test_write_from_list(self):
        p = pathlib.Path('/tmp/a.tsv')
        rows = [['Yamada', 10]]
        f = DsvFile(p, '	')
        f.write(rows)
        self.assertEqual(f.read(), [['Yamada', '10']])
    def test_write_from_namedtuple_named(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=1)
        rows = f.read()
        self.assertEqual(f.read(), [f.RowType('Yamada', '10')])
        rows.append(f.RowType('Kijima', '33'))
        rows.append(f.RowType('Sasaki', '44'))
        f.write(rows)
        self.assertEqual(f.read(), [f.RowType('Yamada', '10'),f.RowType('Kijima', '33'),f.RowType('Sasaki', '44')])

    """
    def test_write_from_dict_typed(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=2)
        rows = f.read_to_dictlist()
        self.assertEqual(f.read(), {'name':'Yamada', 'age':10})
        rows.append({'name':'Kijima', 'age':33})
        rows.append({'name':'Sasaki', 'age':44})
        f.write(rows)
        self.assertEqual(f.read(), [f.RowType('Yamada', 10),f.RowType('Kijima', 33),f.RowType('Sasaki', 44)])
    """

    def test_write_from_namedtuple_typed(self):
        p = pathlib.Path('/tmp/a.tsv')
        p.write_text('''name	age
str	int
Yamada	10''')
        f = DsvFile(p, '	', header_line_num=2)
        rows = f.read()
        self.assertEqual(f.read(), [f.RowType('Yamada', 10)])
        rows.append(f.RowType('Kijima', 33))
        rows.append(f.RowType('Sasaki', 44))
        f.write(rows)
        self.assertEqual(f.read(), [f.RowType('Yamada', 10),f.RowType('Kijima', 33),f.RowType('Sasaki', 44)])

if __name__ == "__main__":
    unittest.main()
