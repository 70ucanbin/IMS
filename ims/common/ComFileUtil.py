import os

def file_upload(file, oldFile, path, year, month, userId, isUpdate=False):
    """添付ファイルのアップロード処理

    すでにファイルがある場合は既存ファイルを削除し、
    新しい添付ファイルを登録します。

    :param file: 添付ファイル。
    :param path: 業務パス・ディレクトリ。
    :param year: 登録年。
    :param month: 登録月。
    :param userId: 登録ユーザID。
    :param isUpdate: ファイルの更新・新規フラグ。
    """

    directory = path + str(year) + "\\" + str(month) + "\\" + userId + "\\"

    if os.path.exists(directory):
        pass
    else:
        os.makedirs(directory)
    if oldFile and isUpdate:
        os.remove(directory + oldFile)
    file.save(directory + file.filename)