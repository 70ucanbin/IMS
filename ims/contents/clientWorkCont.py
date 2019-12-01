
class ClientWorkCalendar:
    """稼働カレンダーの一覧表示用のコンテンツクラス

    :param month: 選択された「月」
    """
    def __init__(self, month=None):
        self.month = month
        self.is_manager = False
        self.userId = None
        self.userName = None
        self.userList = None
        self.monthList = None
        self.calendaDetails = None


class ClientWorkList:
    """稼働カレンダー一覧で選択された日の一覧表示用のコンテンツクラス

    :param month: 選択された「月」
    :param day: 選択された「日」
    :param data: 一覧表示用データ 
    """
    def __init__(self, month=None, day=None, data=None):
        self.is_self = False
        self.month = month
        self.day = day
        self.dataSet = data


class ClientWorkDetails:
    """稼働詳細画面用コンテンツクラス

    :param month: 選択された「月」
    :param day: 選択された「日」
    :param form: データ格納form
    """
    def __init__(self, month=None, day=None, form = None):
        self.is_self = False
        self.month = month
        self.day = day
        self.form = form