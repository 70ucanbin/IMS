
![Preview](https://github.com/70ucanbin/IMS/blob/test_manage_session/backup/sample.gif)

# IMS
技術取得のついでに、このWebアプリを作った。

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

## このWebアプリを通して習得できたもの
- Webアプリを作れるようになった（一人で）
  - システムの全体像をイメージできる能力(脳内で設計しながら作った)
  - 一人で全部実装できる(時間さえあれば)
- バックエンド
  - プログラミング言語Pythonの基本的な使い方
  - postgreSQLのインストール、設定、使用
  - Web Framework: Flaskを使用した開発
  - PythonのORM: sqlalchemyの基本的な使い方
- フロント
  - JavaScriptの基本的な使い方
  - library: DataTablesの基本的な使い方
  - Ajaxの実装
  - Bootstrapの基本的な使い方
- その他
  - VScodeの基本的な使い方
  - リモート開発環境の構築
  - githubの利用