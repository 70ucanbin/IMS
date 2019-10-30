
class TravelExpensesListCont:
    """旅費精算一覧画面用コンテンツクラス
    """
    def __init__(self, month=None, monthList=None):
        self.month = month
        self.is_manager = False
        self.userList = None
        self.monthList = monthList

class TravelExpensesDetailsCont:
    """旅費精算詳細画面用コンテンツクラス
    """
    def __init__(self, month=None, form=None):
        self.month = month
        self.is_self = False
        self.form = form