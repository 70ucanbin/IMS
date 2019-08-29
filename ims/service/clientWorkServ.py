from ims.mappers.clientWorkMapper import selectTraClientWork as getWorkTime
from ims.mappers.clientWorkMapper import selectTraClientWorkList as getList
from ims.mappers.clientWorkMapper import selectTraClientWorkDetails as getDetails
# その日の稼働時間合計値
def getClientWork(employeeId, year, month, day):
    result = getWorkTime(employeeId, year, month ,day)

    return result

def getClientWorkList(employeeId, year, month, day):
    dto = getList(employeeId, year, month ,day)

    return dto

def getClientWorkDetails(clientWorkId):
    dto = getDetails(clientWorkId)

    return dto















def insertUpdateClientWork(isUpdate, **kwargs):
    try:
        dto = TraClientWork(
            kwargs["employee_id"],
            kwargs["work_year"],
            kwargs["work_month"],
            kwargs["work_day"],
            kwargs["order_cd"],
            kwargs["task_cd"],
            kwargs["sub_order_cd"],
            kwargs["work_time"],
            kwargs["note"]
        )
        insertUpdateTraClientWork(dto,isUpdate)

    except:
        print('なんかうまくいかなかった')