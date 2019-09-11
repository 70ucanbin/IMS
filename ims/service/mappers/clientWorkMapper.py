from ims.service.mappers.models.traClientWork import TraClientWork as __model
from ims.service.mappers.models.comItem import ComItem
from ims import db
from sqlalchemy import and_
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError

# 稼働日の稼働時間合計を取得
def selectTraClientWork(employeeId, year, month, day):
    workTime = db.session.query(
        db.func.to_char(db.func.sum(__model.work_time),'HH24:MI').label('workTime')
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
        __model.client_work_id.label('clientWorkId'),
        db.func.to_char(__model.work_time,'HH24:MI').label('workTime'),
        orderCd.item_value.label('orderCd'),
        taskCd.item_value.label('taskCd'),
        subOrderCd.item_value.label('subOrderCd') 
        ).filter(
            __model.employee_id == employeeId,
            __model.work_year == year,
            __model.work_month == month,
            __model.work_day == day
        ).outerjoin(
            (orderCd,
            and_(orderCd.item_key == __model.order_cd,
            orderCd.item_category =='1')),
            (subOrderCd,
            and_(subOrderCd.item_key == __model.sub_order_cd,
            subOrderCd.item_category =='2')),
            (taskCd,
            and_(taskCd.item_key == __model.task_cd,
            taskCd.item_category =='3'))
        ).all()

    return clientworkList

def selectTraClientWorkDetails(clientWorkId):
    clientwork = db.session.query(
        __model.client_work_id.label('clientWorkId'),
        func.to_number(func.to_char((__model.work_time),'HH24'), '999999').label('workHours'),
        func.to_number(func.to_char((__model.work_time),'MI'), '999999').label('workMinutes'),
        __model.order_cd.label('orderCd'),
        __model.task_cd.label('taskCd'),
        __model.sub_order_cd.label('subOrderCd'),
        __model.note
        ).filter_by(
            client_work_id = clientWorkId
        ).first()
    return clientwork

def insertUpdateTraClientWork(dto,isUpdate):

    model = __model()
    model.employee_id = dto['employeeId'],
    model.work_year = dto['year'],
    model.work_month = dto['month'],
    model.work_day = dto['day'],
    model.order_cd = dto['orderCd'],
    model.task_cd = dto['taskCd'],
    model.sub_order_cd = dto['subOrderCd'],
    model.work_time = dto['workTime'],
    model.note = dto['note'] or ""

    try:
        if isUpdate:
            model.client_work_id = dto['clientWorkId']
            db.session.merge(model)
        else:
            db.session.add(model)
        db.session.flush()
        result = {'success':True}

    except IntegrityError:
        db.session.rollback()
        result = {'success':False,'message':'他のユーザが先に更新しました。'}

    return result


def deleteTraClientWork(clientWorkId):
    # try:
        dto = __model.query.get(clientWorkId)
        db.session.delete(dto)
        test = __model.query.filter_by(client_work_id = clientWorkId).delete()
        print(test)
        db.session.flush()
        result = {'success':True}
    # except IntegrityError:
        # db.session.rollback()
        # result = {'success':False,'message':'他のユーザが先に更新しました。'}
        return result