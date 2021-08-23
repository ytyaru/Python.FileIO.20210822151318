#!/usr/bin/env python3
# coding: utf8
import os, sys, pathlib, csv, json, datetime, locale
from abc import ABCMeta, abstractmethod
from string import Template
from collections import namedtuple
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
        print(self.__header_line_num)
    @property
    def Delimiter(self): return self.__delimiter
    @property
    def Names(self): return self.__names
    @Names.setter
    def Names(self, v): self.__names = v
    @property
    def Types(self): return self.__types
    @Names.setter
    def Types(self, v): self.__types = v
    @property
    def RowType(self): return self.__row_type
    def read(self):
        with open(self.Path, mode='r', encoding=self.Encoding) as f:
            reader = csv.reader(f, delimiter=self.Delimiter)
            print(self.__header_line_num)
            if 0 < self.__header_line_num: self.Names = next(reader)
            if 1 < self.__header_line_num: self.Types = next(reader)
#            if 0 < self.__header_line_num: self.Names = list(next(reader))
#            if 1 < self.__header_line_num: self.Types = list(next(reader))
            for row in reader: yield row
#            return list(rows)
    def read_to_namedtuple(self):
        with open(self.Path, mode='r', encoding=self.Encoding) as f:
            reader = csv.reader(f, delimiter=self.Delimiter)
            if 0 < self.__header_line_num: self.Names = next(reader)
            if 1 < self.__header_line_num: self.Types = next(reader)
            if not self.Names: return None
            self.__row_type = T = namedtuple('CsvRow', ' '.join(self.Names))
            for row in rows:
                yield [T(*c) for c in row]
    def read_to_named_and_typed(self):
        with open(self.Path, mode='r', encoding=self.Encoding) as f:
            reader = csv.reader(f, delimiter=self.Delimiter)
            if 0 < self.__header_line_num: self.Names = next(reader)
            if 1 < self.__header_line_num: self.Types = next(reader)
            if not self.Names: return None
            self.__row_type = T = namedtuple('CsvRow', ' '.join(self.Names))
            for row in rows:
                for i, c in enumerate(row):
                    values = [eval(f'{self.Types[i]}("{c}")') for i,c in enumerate(row)]
                    yield T(*values)
    def read_to_dictlist(self):
        rows = self.read()
        if not self.Names: return rows
        dl = []
        for r in rows:
            dl.append(dict([(self.Names[i], c) for i,c in enumerate(r)]))
        return dl
    def write(self, content):
        super().write(content)
        rows = csv.write(delimiter=self.Delimiter)

class CsvFile(File):
    def read(self):
        pass
    def write(self, content):
        super().write(content)
class TsvFile(File):
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
