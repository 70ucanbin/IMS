from ims.mappers.clientWorkMapper import selectTraClientWork

def getClientWork(employeeId, year, month, day):

    return selectTraClientWork(employeeId, year, month ,day)