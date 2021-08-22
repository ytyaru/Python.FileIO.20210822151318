#!/usr/bin/env python3
# coding: utf8
import os,sys,pathlib,inspect
sys.path.append(str(pathlib.Path(__file__, '../../src').resolve()))
from file import File
import unittest
from unittest.mock import MagicMock, patch, mock_open
class TestFile(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError, msg="Can't instantiate abstract class File with abstract methods read, write"):
            f = File()

if __name__ == "__main__":
    unittest.main()
