#!/usr/bin/env python3
# coding: utf8
import os,sys,pathlib,inspect
sys.path.append(str(pathlib.Path(__file__, '../../src').resolve()))
from file import FileObject
import unittest
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

if __name__ == "__main__":
    unittest.main()
