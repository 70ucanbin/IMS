
class DayDetails:
    def __init__(self, day=None, disabled=None, details=None, rest_flg=None):
        self.day = day
        self.disabled = disabled
        self.details = details
        self.rest_flg = rest_flg


    def __repr__(self):
        return '<Day day:{}>'.format(self.day)

class MasterDataList:
    def __init__(self, categoryList):
        self.categoryList = categoryList
        self.dataCategory = None
        if categoryList[0]:
            self.dataCategory = categoryList[0]

class MasterDetails:
    def __init__(self, form=None):
        self.form = form