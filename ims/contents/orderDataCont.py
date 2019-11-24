
class OrderDataList:
    """件名大分類一覧表示用のコンテンツクラス

    :param data: 一覧表示用データ 
    """
    def __init__(self, data=None):
        self.dataSet = data

class Details:
    """件名大分類・小分類詳細表示用のコンテンツクラス

    :param form: 詳細画面form
    """
    def __init__(self, form=None):
        self.form = form

class SubOrderDataList:
    """件名小分類一覧表示用のコンテンツクラス

    :param data: 一覧表示用データ 
    """
    def __init__(self, orderList):
        self.orderList = orderList
        self.dataOrderCd = None
        if orderList[0]:
            self.dataOrderCd = orderList[0]