
class MonthlyReportCalendar:
    """月報カレンダーの一覧表示用のコンテンツクラス

    :param month: 選択された「月」
    """
    def __init__(self, month=None):
        self.month = month
        self.userId = None
        self.userName = None
        self.userList = None
        self.monthList = None
        self.calendaDetails = None


class MonthlyReportDetails:
    """月報詳細画面用コンテンツクラス

    :param month: 選択された「月」
    :param day: 選択された「日」
    """
    def __init__(self, month=None, day=None):
        self.is_self = False
        self.is_update = False
        self.month = month
        self.day = day
        self.form = None
