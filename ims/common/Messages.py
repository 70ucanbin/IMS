
class Messages():
    SUCCESS_INSERTED = 'データを作成しました。'
    SUCCESS_UPDATED = 'データを更新しました。'
    SUCCESS_DELETED = '指定されたデータを削除しました。'
    WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED = '指定されたデータは存在しません。他のユーザにより変更・削除されていないか確認してください。'
    WARNING_UNIQUE_CONSTRAINT = '作成しようとしたデータは既に存在しています。'

    LOGIN_FAILED = 'usernameまたはPasswordが異なります'

    NO_DATA_AVAILABLE = 'データがありません。'

    NO_FOUND_ORDER = '大分類データがありません、小分類を作成するには先に大分類を作成してください。'

    # message style
    SUCCESS_CSS = 'list-group-item list-group-item-success'
    WARNING_CSS = 'list-group-item list-group-item-warning'
    DANGER_CSS = 'list-group-item list-group-item-danger'