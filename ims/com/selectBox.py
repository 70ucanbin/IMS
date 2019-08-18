
class _SelectBox:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

class MonthList(object):
    def __init__(self, startingPoint=0, endPoint=0, step=0):
        self._monthRange = list(range(startingPoint, endPoint, step))
        self.selectList = list()
    
        for month in self._monthRange:
            self.selectList.append(_SelectBox(month, str(month).zfill(2)))

class HoursList(object):
    def __init__(self, startingPoint=0, endPoint=0, step=0):
        self._hoursRange = list(range(startingPoint, endPoint, step))
        self.selectList = list()
    
        for hours in self._hoursRange:
            self.selectList.append(_SelectBox(hours, str(hours).zfill(2)))

class MinutesList(object):
    def __init__(self, startingPoint=0, endPoint=0, step=0):
        self._minutesRange = list(range(startingPoint, endPoint, step))
        self.selectList = list()
    
        for minutes in self._minutesRange:
            self.selectList.append(_SelectBox(minutes, str(minutes).zfill(2)))
