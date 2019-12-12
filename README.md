
![Preview](https://user-images.githubusercontent.com/45325385/70678312-0ecab980-1cd5-11ea-9c09-42626c2f65dd.gif)

# IMS

技術取得のついでに、社内管理を楽にしたいと思い、このWebアプリを作った。

IMSは内部管理システムっていう意味で適当に付けた名前。

## Requires

必要なものを先にインストールしてください。
  - Python Version = "3.7"
  - PostgreSQL Version = "10" or "11"
  - pipenv

## Installation

必要なlibraryをインストール：`pipenv install`

[config.py](https://github.com/70ucanbin/IMS/blob/master/config.py)の設定変更(DB接続情報、SECRET_KEY)

script実行:

```bash
$ export FLASK_APP=init_create.py
$ FLASK create
```

DBにテーブルとシーケンスが作られたことを確認できればOK

## Getting started
start up:
```bash
$ pipenv shell
$ python server.py
```
