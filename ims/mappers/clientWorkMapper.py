from ims.mappers.models.traClientWork import TraClientWork
from ims import db
from sqlalchemy import text
from sqlalchemy.sql import func
from ims.mappers.sql.clientWorkSql import selectTraClientWorkList

# 稼働日の稼働時間合計を取得
def selectTraClientWork(employeeId, year, month, day):
    workTime = db.session.query(
        db.func.to_char(db.func.sum(TraClientWork.work_time),'HH24:MI').label('workTime')
        ).filter_by(
            employee_id = employeeId,
            work_year = year,
            work_month = month,
            work_day = day
        ).scalar()
    return workTime

# 選択された日の稼働情報を取得
def selectTraClientWorkList(employeeId, year, month, day):
    sql = selectTraClientWorkList()
    clientworkList = db.engine.execute(text(sql), 
        {'employeeId':employeeId,'workYear':year,'workMonth':month,'workDay':day})
    return clientworkList

def selectTraClientWorkDetails(clientWorkId):
    clientwork = db.session.query(
        TraClientWork.client_work_id.label('clientWorkId'),
        func.to_number(func.to_char((TraClientWork.work_time),'HH24'), '999999').label('workHours'),
        func.to_number(func.to_char((TraClientWork.work_time),'MI'), '999999').label('workMinutes'),
        TraClientWork.order_cd.label('orderCd'),
        TraClientWork.task_cd.label('taskCd'),
        TraClientWork.sub_order_cd.label('subOrderCd'),
        TraClientWork.note
        ).filter_by(
            client_work_id = clientWorkId
        ).first()
    return clientwork

def insertUpdateTraClientWork(traClientwork,isUpdate):

    if isUpdate:
        db.session.merge(traClientwork)
    else:
        db.session.add(traClientwork)
