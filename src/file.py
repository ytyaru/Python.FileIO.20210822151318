#!/usr/bin/env python3
# coding: utf8
import os, sys, pathlib, csv, json, datetime, locale
from abc import ABCMeta, abstractmethod
from string import Template
from collections import namedtuple
# 以下CSVのヘッダで使う型
from decimal import Decimal
from datetime import datetime, date, time, timedelta, tzinfo, timezone
from urllib.parse import urlparse as url
from pathlib import Path as path
"""
class FileReader:
    @classmethod
    @Null.exept
    def text(self, path):
        with open(path, mode='r', encoding='utf-8') as f: return f.read().rstrip('\n')
    @classmethod
    def json(self, path):
        with open(path, mode='r', encoding='utf-8') as f: return json.load(f)
class File:
    def __init__(self, path):
        self.__path = path
    @property
    def Text(self):
        with open(path, mode='r', encoding='utf-8') as f: return f.read().rstrip('\n')
    @Text.setter
    def Text(self, v):
        with open(path, mode='w', encoding='utf-8') as f: f.write(v)
"""
        
class FileObject:
    def __init__(self, path):
        self.__path = path
        self.__enc = 'utf-8'
    @property
    def Path(self): return self.__path
    @Path.setter
    def Path(self, v): self.__path = v
    @property
    def Encoding(self): return self.__enc
    @Encoding.setter
    def Encoding(self, v): self.__enc = v
    @property
    def Exist(self): return os.path.exists(self.Path)

#open mode = r, r+, w, a, x
class File(FileObject, metaclass=ABCMeta):
    @property
    def Exist(self): return os.path.isfile(self.Path)
    @abstractmethod
    def read(self): pass
    @abstractmethod
    def write(self, content):
        # 途中までのディレクトリを生成する
        parent = pathlib.Path(self.Path).parent
        if not parent.is_dir(): parent.mkdir(parents=True)
class BinaryFile(File):
    def read(self):
        with open(self.Path, mode='rb') as f: return f.read()
    def write(self, content):
        super().write(content)
        with open(self.Path, mode='wb') as f: f.write(content)
    def over_write(self, content, pos=0):
        super().write(content)
        with open(self.Path, mode='r+') as f:
            f.seek(pos)
            f.write(content)
class TextFile(File):
    def read(self):
        with open(self.Path, mode='r', encoding=self.Encoding) as f:
            return f.read().rstrip('\n')
    def write(self, content):
        super().write(content)
        with open(self.Path, mode='w', encoding=self.Encoding) as f:
            f.write(content)
    def append(self, content):
        super().write(content)
        with open(self.Path, mode='a', encoding=self.Encoding) as f:
            f.write('\n'.join(content))
class LineTextFile(File):
    def read(self):
        with open(self.Path, mode='r', encoding=self.Encoding) as f:
            return [l.rstrip('\n') for l in f.readlines()]
    def write(self, content):
        super().write(content)
        with open(self.Path, mode='w', encoding=self.Encoding) as f:
            f.write('\n'.join(content))
    def append(self, content):
        super().write(content)
        with open(self.Path, mode='a', encoding=self.Encoding) as f:
            f.write('\n'.join(content))
    def insert(self, content, line_no=0):
        super().write(content)
        l = self.read()
        l[line_no:line_no] = content
        with open(self.Path, mode='w', encoding=self.Encoding) as f:
            f.writelines([line+'\n' for line in l])

class DsvFile(File):
    def __init__(self, path, delimiter, header_line_num=0):
        super().__init__(path)
        self.__header_line_num = header_line_num
        self.__reader = self.__create_reader(path, delimiter, header_line_num)
    def __create_reader(self, p, d, h):
        return TypedDsvFile(p, d, h) if 2 == h else \
               NamedDsvFile(p, d, h) if 1 == h else \
               ListedDsvFile(p, d, h)
    @property
    def Delimiter(self): return self.__reader.Delimiter
    @property
    def Names(self): return self.__reader.Names
    @property
    def Types(self): return self.__reader.Types
    @property
    def RowType(self): return self.__reader.RowType
    def read(self):
        return self.__reader.read()
    def select(self, *args, **kwargs):
        return self.__reader.select(*args, **kwargs)
    def read_to_list(self):
        return self.__reader.read_to_list()
    def read_to_dictlist(self):
        return self.__reader.read_to_dict()
    def read_to_namedtuple(self):
        return self.__reader.read_to_namedtuple()
    def write(self, content):
        return self.__reader.write(content)
#        super().write(content)
#        rows = csv.write(delimiter=self.Delimiter)
class DsvFileReader(File):
    def __init__(self, path, delimiter, header_line_num):
        super().__init__(path)
        self.__delimiter = delimiter
        self.__header_line_num = header_line_num
        self.__names = []
        self.__types = []
        self.__row_type = None
    @property
    def Delimiter(self): return self.__delimiter
    @property
    def Names(self): return self.__names
    @property
    def Types(self): return self.__types
    @property
    def RowType(self): return self.__row_type
    def open(self):# https://docs.python.org/ja/3/library/csv.html#id3
        return open(self.Path, mode='r', encoding=self.Encoding, newline='') 
    def read_header(self, f):
        reader = csv.reader(f, delimiter=self.Delimiter)
        if 0 < self.__header_line_num:
            self.__names = next(reader)
            self.__row_type = namedtuple('Row', ' '.join(self.Names))
        if 1 < self.__header_line_num:
            self.__types = next(reader)
        return reader
    def cast(self, i, c):
        return eval(f'{self.Types[i]}("{c}")', globals(), locals())
    def read(self): pass
    def write(self, rows):
        if not isinstance(rows, list): raise ValueError('引数は二重配列にしてください。')
        if len(rows) < 1: raise ValueError('要素がありません。引数の配列に1つ以上要素を加えてください。')
        if len(rows[0]) < 1: raise ValueError('要素がありません。引数の配列に1つ以上要素を加えてください。')

class ListedDsvFile(DsvFileReader):
    def __init__(self, path, delimiter, header_line_num=0):
        super().__init__(path, delimiter, header_line_num)
    def read(self):
        with self.open() as f:
            return list(self.read_header(f))
    def read_to_list(self): return self.read()
    def read_to_dict(self): return self.read()
    def read_to_namedtuple(self): return self.read()
    def select(self, *args, **kwargs):
        with self.open() as f:
            reader = self.read_header(f)
            selecteds = []
            for row in reader:
                if all([True if a is None else row[i] == a for i,a in enumerate(args)]):
                    selecteds.append(row)
            return selecteds
    def write(self, rows):
        super().write(rows)
        with open(self.Path, mode='w', encoding=self.Encoding, newline='') as f:
            f.writelines([f'{self.Delimiter.join([str(c) for c in row])}{os.linesep}' for row in rows])

class NamedDsvFile(DsvFileReader):
    def __init__(self, path, delimiter, header_line_num):
        super().__init__(path, delimiter, header_line_num)
    def read(self):
        with self.open() as f:
            return [self.RowType(*row) for row in self.read_header(f)]
    def read_to_list(self):
        with self.open() as f:
            return list(self.read_header(f))
    def read_to_dict(self):
        with self.open() as f:
            return [dict([(self.Names[i], c) for i,c in enumerate(r)]) for r in self.read_header(f)]
    def read_to_namedtuple(self):
        with self.open() as f:
            return [self.RowType(*r) for r in self.read_header(f)]
    def select(self, *args, **kwargs):
        with self.open() as f:
            reader = self.read_header(f)
            selecteds = []
            for row in reader:
                r = self.RowType(*row)
                if all([v(getattr(r, k)) if callable(v) else getattr(r, k) == v for k,v in kwargs.items()]):
                    selecteds.append(r)
            return selecteds
    def write(self, rows):
        super().write(rows)
        with open(self.Path, mode='w', encoding=self.Encoding, newline='') as f:
            f.write(f'{self.Delimiter.join(self.Names)}{os.linesep}')
            f.writelines([f'{self.Delimiter.join([str(c) for c in row])}{os.linesep}' for row in rows])

class TypedDsvFile(DsvFileReader):
    def __init__(self, path, delimiter, header_line_num):
        super().__init__(path, delimiter, header_line_num)
    def read(self): return self.read_to_namedtuple()
    def read_to_list(self):
        with self.open() as f:
            return list(self.read_header(f))
    def read_to_dict(self):
        with self.open() as f:
            return [dict([(self.Names[i], self.cast(i,c)) for i,c in enumerate(r)]) for r in self.read_header(f)]
    def read_to_namedtuple(self):
        with self.open() as f:
            return [self.RowType(*[self.cast(i,c) for i,c in enumerate(row)]) for row in self.read_header(f)]
    def select(self, *args, **kwargs):
        with self.open() as f:
            reader = self.read_header(f)
            selecteds = []
            for row in reader:
                r = self.RowType(*[self.cast(i,c) for i,c in enumerate(row)])
                if all([v(getattr(r, k)) if callable(v) else getattr(r, k) == v for k,v in kwargs.items()]):
                    selecteds.append(r)
            return selecteds
    def write(self, rows):
        super().write(rows)
        with open(self.Path, mode='w', encoding=self.Encoding, newline='') as f:
            f.write(f'{self.Delimiter.join(self.Names)}{os.linesep}')
            f.write(f'{self.Delimiter.join(self.Types)}{os.linesep}')
            f.writelines([f'{self.Delimiter.join([str(c) for c in row])}{os.linesep}' for row in rows])

class CsvFile(DsvFile):
    def __init__(self, path, header_line_num=0):
        super.__init__(path, ',', header_line_num=header_line_num)
class TsvFile(DsvFile):
    def __init__(self, path, header_line_num=0):
        super.__init__(path, '\t', header_line_num=header_line_num)

class JsonFile(File):
    def read(self):
        pass
    def write(self, content):
        super().write(content)
    
class Directory(FileObject):
    @property
    def Exist(self): return os.path.isdir(self.Path)
    def make(self):
        this = pathlib.Path(self.Path)
        if not this.is_dir(): parent.mkdir(parents=True)


class Link(FileObject):
    pass
