from ims.mappers.models.traClientWork import TraClientWork
from ims.mappers.models.comItem import ComItem
from ims import db
from sqlalchemy import text, and_
from sqlalchemy.sql import func
from ims.mappers.sql.clientWorkSql import selectClientWorkJoinCom
from sqlalchemy.orm import aliased

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
    orderCd = aliased(ComItem)
    taskCd = aliased(ComItem)
    subOrderCd = aliased(ComItem)

    clientworkList = db.session.query( 
        TraClientWork.client_work_id.label('clientWorkId'),
        db.func.to_char(TraClientWork.work_time,'HH24:MI').label('workTime'),
        orderCd.item_value.label('orderCd'),
        taskCd.item_value.label('taskCd'),
        subOrderCd.item_value.label('subOrderCd') 
        ).filter(
            TraClientWork.employee_id == employeeId,
            TraClientWork.work_year == year,
            TraClientWork.work_month == month,
            TraClientWork.work_day == day
        ).outerjoin(
            (orderCd,
            and_(orderCd.item_key == TraClientWork.order_cd,
            orderCd.item_category =='1')),
            (subOrderCd,
            and_(subOrderCd.item_key == TraClientWork.sub_order_cd,
            subOrderCd.item_category =='2')),
            (taskCd,
            and_(taskCd.item_key == TraClientWork.task_cd,
            taskCd.item_category =='3'))
        ).all()

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
        result = db.session.merge(traClientwork)
    else:
        result = db.session.add(traClientwork)
        result = db.session.flush()
    return result
