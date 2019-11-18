
class OrderDataList:
    """件名大分類一覧表示用のコンテンツクラス

    :param data: 一覧表示用データ 
    """
    def __init__(self, data=None):
        self.dataSet = data

class OrderDetails:
    def __init__(self, form=None):
        self.form = form

class SubOrderDataList:
    """件名小分類一覧表示用のコンテンツクラス

    :param data: 一覧表示用データ 
    """
    def __init__(self, orderList):
        self.orderList = orderList
        self.dataCategory = None
        if orderList[0]:
            self.dataCategory = orderList[0]

class SubOrderDetails:
    def __init__(self, form=None):
        self.form = form