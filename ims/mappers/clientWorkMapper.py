from ims.mappers.models.traClientWork import TraClientWork
from ims import db
from sqlalchemy import text

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

# 稼働日の稼働時間合計を取得
def selectTraClientWorkList(employeeId, year, month, day):

    clientworkList = db.session.query(
        TraClientWork.client_work_id.label('clientWorkId'),
        db.func.to_char((TraClientWork.work_time),'HH24:MI').label('workTime'),
        TraClientWork.order_cd.label('orderCd'),
        TraClientWork.task_cd.label('taskCd'),
        TraClientWork.sub_order_cd.label('subOrderCd')
        ).filter_by(
            employee_id = employeeId,
            work_year = year,
            work_month = month,
            work_day = day
        ).all()
    
    
    
    # TraClientWork.query.filter_by(
    #     employee_id=employeeId,
    #     work_year = year,
    #     work_month = month,
    #     work_day = day
    # ).all()

    return clientworkList

def insertUpdateTraClientWork(traClientwork,isUpdate):

    if isUpdate:
        db.session.merge(traClientwork)
    else:
        db.session.add(traClientwork)
