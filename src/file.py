#!/usr/bin/env python3
# coding: utf8
import os, sys, csv, json, datetime, locale
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
        with open(path, mode='rb', encoding=self.Encoding) as f: return f.read()
    def write(self, content):
        super().write(content)
        with open(path, mode='wb', encoding=self.Encoding) as f: f.write(v)
class TextFile(File):
    def read(self):
        with open(self.Path, mode='r', encoding=self.Encoding) as f:
            return f.read().rstrip('\n')
    def write(self, content):
        super().write(content)
        with open(path, mode='w', encoding=self.Encoding) as f:
            f.write(v)
class LineTextFile(File):
    def read(self):
        with open(path, mode='r', encoding=self.Encoding) as f:
            return f.readlines()
    def write(self, content):
        super().write(content)
        with open(path, mode='w', encoding=self.Encoding) as f:
            f.write('\n'.join(v))
    def append(self, content):
        super().write(content)
        with open(path, mode='a', encoding=self.Encoding) as f:
            f.write('\n'.join(v))
#        parent = pathlib.Path(self.Path).parent
#        if not parent.is_dir(): raise FileNotFoundError(f'{self.Path}が存在しません。')
    def insert(self, content, line_no=0):
        super().write(content)
        with open(path, mode='r', encoding=self.Encoding) as f:
            l = f.readlines()
        l[line_no:line_no] = content
#        for c in content.reverse():
#            l.insert(line_no, c)
        with open(path, mode='w', encoding=self.Encoding) as f:
            f.writelines(l)
#        parent = pathlib.Path(self.Path).parent
#        if not parent.is_dir(): raise FileNotFoundError(f'{self.Path}が存在しません。')
class CsvFile(File):
    @property
    def Exist(self): return os.path.exists()
    @property
    def Names(self): return self.__names
    @Names.setter
    def Names(self, v): self.__names = v
    @property
    def Types(self): return self.__types
    @Names.setter
    def Types(self, v): self.__types = v
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
