
class UserListCont:
    """ユーザー情報一覧画面用コンテンツクラス

    :param form: データ格納form
    """
    def __init__(self, dataSet=None):
        self.dataSet = dataSet

class UserDetailsCont:
    """ユーザー情報詳細画面用コンテンツクラス

    :param form: データ格納form
    """
    def __init__(self, form=None):
        self.form = form