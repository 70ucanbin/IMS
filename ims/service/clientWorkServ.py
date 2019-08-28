from ims.mappers.clientWorkMapper import selectTraClientWork, insertUpdateTraClientWork, selectTraClientWorkList
from ims.mappers.models.traClientWork import TraClientWork

def getClientWork(employeeId, year, month, day):
    dto = selectTraClientWork(employeeId, year, month ,day)
    if dto:
        workTime = '稼働時間' + dto
    else:
        workTime = ''
    return workTime

def getClientWorkList(employeeId, year, month, day):
    dto = selectTraClientWorkList(employeeId, year, month ,day)

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