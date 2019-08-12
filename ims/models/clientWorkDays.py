

class ClientWorkDay:
    __tablename__ = 'clientWorkDays'
    def __init__(self, day=None, disabled=None):
        self.day = day
        self.disabled = disabled