from ims.service.mappers.models.traClientWork import TraClientWork as __model
from ims.service.mappers.models.comItem import ComItem
from ims import db

from sqlalchemy import and_, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError


def selectWorkMonthDetails(userId, year, month, startDay, endDay):
    """選択された月の日別とその稼働時間を取得するDB処理

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param startDay: 月の初日
    :param endDay: 月の最後の日
    """
    subq1 = db.session.query(
        func.generate_series(
            func.date(startDay) - func.CURRENT_DATE(), func.date(endDay) - func.CURRENT_DATE()
        ).label('i')
    ).subquery()

    subq2 = db.session.query(
        func.cast(func.date_part('day',  func.CURRENT_DATE() + subq1.c.i ), Integer).label('day')
    ).subquery()
    
    workMonthDetails = db.session.query(
        subq2.c.day,
        db.func.to_char(db.func.sum(__model.work_time),'HH24:MI').label('workTime')
    ).outerjoin(__model, 
        and_(
        subq2.c.day == __model.work_day,
        __model.user_id == userId)
    ).group_by(
        subq2.c.day
    ).order_by(
        subq2.c.day
    ).all()

    return workMonthDetails

def selectTraClientWork(userId, year, month, day):
    """選択された日の稼働時間を取得するDB処理

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
    workTime = db.session.query(
        db.func.to_char(db.func.sum(__model.work_time),'HH24:MI').label('workTime')
        ).filter_by(
            user_id = userId,
            work_year = year,
            work_month = month,
            work_day = day
        ).scalar()
    return workTime

# 選択された日の稼働情報を取得
def selectTraClientWorkList(userId, year, month, day):
    """選択された日の稼働リストを取得するDB処理

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
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
            __model.user_id == userId,
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
    """選択された稼働詳細を取得するDB処理

    :param clientWorkId: 稼働詳細ID
    """
    clientwork = db.session.query(
        __model.client_work_id.label('clientWorkId'),
        __model.user_id.label('userId'),
        __model.work_month.label('workMonth'),
        __model.work_day.label('workDay'),
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
    """稼働詳細の新規または修正を処理するDB処理
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 稼働詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __model()
    model.user_id = dto['userId'],
    model.work_year = dto['year'],
    model.work_month = dto['month'],
    model.work_day = dto['day'],
    model.order_cd = dto['orderCd'],
    model.task_cd = dto['taskCd'],
    model.sub_order_cd = dto['subOrderCd'],
    model.work_time = dto['workTime'],
    model.note = dto['note'] or ""

    if isUpdate:
        model.client_work_id = dto['clientWorkId']
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()


def deleteTraClientWork(clientWorkId):
    """稼働詳細を削除するDB処理
    サービス層のExceptionをキャッチし、処理します。

    :param clientWorkId: 稼働詳細ID
    """
    __model.query.filter_by(client_work_id = clientWorkId).delete()
    db.session.flush()