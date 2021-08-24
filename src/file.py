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
        self.__delimiter = delimiter
        self.__header_line_num = header_line_num
        self.__names = []
        self.__types = []
    @property
    def Delimiter(self): return self.__delimiter
    @property
    def Names(self): return self.__names
    @Names.setter
    def Names(self, v): self.__names = v
    @property
    def Types(self): return self.__types
    @Types.setter
    def Types(self, v): self.__types = v
    @property
    def RowType(self): return self.__row_type
    def __read_header(self, f):
        reader = csv.reader(f, delimiter=self.Delimiter)
        if 0 < self.__header_line_num: self.Names = next(reader)
        if 1 < self.__header_line_num: self.Types = next(reader)
        return reader
    def __cast(self, i, c): return eval(f'{self.Types[i]}("{c}")', globals(), locals())
    def read(self):
        with open(self.Path, mode='r', encoding=self.Encoding, newline='') as f:# https://docs.python.org/ja/3/library/csv.html#id3
            reader = self.__read_header(f)
            if not self.Names: return list(reader)
            self.__row_type = T = namedtuple('Row', ' '.join(self.Names))
            rows = []
            for row in reader:
                if self.Types: rows.append(T(*[self.__cast(i,c) for i,c in enumerate(row)]))
                else: rows.append(T(*row))
            return rows
    def select(self, *args, **kwargs):
        with open(self.Path, mode='r', encoding=self.Encoding, newline='') as f:
            reader = self.__read_header(f)
            if self.Names: self.__row_type = T = namedtuple('CsvRow', ' '.join(self.Names))
            selecteds = []
            for row in reader:
                if self.Names:
                    r = [T(*c) for c in row]
                    if all([getattr(r, k) == v for k,v in kwargs.items()]):
                        selecteds.append(r)
                else:
                    if all([row[i] == a[i] for i,a in enumerate(args)]):
                        selecteds.append(row)
            return selecteds
    def read_to_list(self):
        with open(self.Path, mode='r', encoding=self.Encoding, newline='') as f:# https://docs.python.org/ja/3/library/csv.html#id3
            reader = self.__read_header(f)
            return list(reader)
    def read_to_namedtuple(self):
        if self.__header_line_num < 1: raise ValueError('header_line_numが1より小さいです。1以上にしてください。')
        l = []
        with open(self.Path, mode='r', encoding=self.Encoding, newline='') as f:
            reader = self.__read_header(f)
            self.__row_type = T = namedtuple('Row', ' '.join(self.Names))
            for row in reader:
                if self.Types: l.append(T(*[self.__cast(i,c) for i,c in enumerate(row)]))
                else: l.append(T(*row))
        return l
    def read_to_dictlist(self):
        if self.__header_line_num < 1: raise ValueError('header_line_numが1より小さいです。1以上にしてください。')
        dl = []
        with open(self.Path, mode='r', encoding=self.Encoding, newline='') as f:
            reader = self.__read_header(f)
            for r in reader:
                if not self.Types: dl.append(dict([(self.Names[i], c) for i,c in enumerate(r)]))
                else: dl.append(dict([(self.Names[i], self.__cast(i,c)) for i,c in enumerate(r)]))
        return dl                     
    def write(self, content):
        super().write(content)
        rows = csv.write(delimiter=self.Delimiter)

class CsvFile(DsvFile):
    def __init__(self, path, header_line_num=0):
        super(path, ',', header_line_num=header_line_num)
    def read(self):
        pass
    def write(self, content):
        super().write(content)
class TsvFile(File):
    def __init__(self, path, header_line_num=0):
        super(path, '\t', header_line_num=header_line_num)
    def read(self):
        pass
    def write(self, content):
        super().write(content)
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
