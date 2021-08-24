# csv

* none-header
    * none-name,str
    * none-name,auto-type
* header
    * name,none-type
    * none-name,type
    * name,type
* row-type
    * list/tuple
    * dict/namedtuple

# 組み込み型

* https://docs.python.org/ja/3/library/stdtypes.html

# 型の自動判定

型|regex
--|-----
`int|`[1-9]([0-9])*`
`decimal`|`(\d)*\.(\d)+`
`date`|`[1-9]([0-9])*[\-/]\d{2}[\-/]\d{2}`
`time`|`\d{2}:\d{2}(:\d{2})?`
`datetime`|`[1-9]([0-9])*[\-/]\d{2}[\-/]\d{2}T\d{2}:\d{2}(:\d{2})?[\-+]\d{2}:\d{2}` （`datetime.datetime.fromisoformat()`）
`url`|上記以外すべて（型が`url`と明示されている）
`path`|上記以外すべて（型が`path`と明示されている）
`str`|上記以外すべて（型が`str`と明示されている。または省略されている）

## 対象外

型|理由
--|----
`float`|丸め誤差が生じてしまうから。
`bytes`|テキスト形式のほうが運用しやすいから。

型|理由
--|----
`tuple`|配列で代用する。更新するときはミュータブルである配列である必要がある
`dict`|名前はCSVのヘッダで十分。`str`型で内容をJSON形式にすれば十分。



