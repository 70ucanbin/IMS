
![Preview](https://user-images.githubusercontent.com/45325385/70678312-0ecab980-1cd5-11ea-9c09-42626c2f65dd.gif)

> ℹ INFO: **このプロジェクトは技術取得のついでに、社内管理を楽にすることを目的に作ったものです。bugを見つかった場合は修正しますが、機能の追加や改修は気分次第です。

## Features

imsはflaskを用いて作ったweb applicationです。

現場の稼働詳細、月報、旅費精算といった社内の作業をサポートし、余計なexcel作業から解放できます。

## Requires

必要なものを先にインストールしてください。
  - Python Version = "3.7*"
  - PostgreSQL Version = "10" or "11"
  - pipenv

## Installation

1. 必要なlibraryをインストール：`pipenv install`

1. [config.py](https://github.com/70ucanbin/IMS/blob/master/config.py)の設定変更(DB接続情報、SECRET_KEY)

1. script実行:

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
