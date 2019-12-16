
class TravelExpensesListCont:
    """旅費精算一覧画面用コンテンツクラス

    :param month: 選択された「月」
    :param monthList: 画面選択用「月」のcomboboxの値
    """
    def __init__(self, month=None, monthList=None):
        self.month = month
        self.userList = None
        self.monthList = monthList

class TravelExpensesDetailsCont:
    """旅費精算詳細画面用コンテンツクラス

    :param month: 選択された「月」
    :param form: データ格納form
    """
    def __init__(self, month=None, form=None):
        self.month = month
        self.is_self = False
        self.form = form