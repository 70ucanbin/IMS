from sqlalchemy import and_, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError

from ims import db
from ims.service.mappers.models.traClientWork import TraClientWork as __model
from ims.service.mappers.models.traOrderData import TraOrder, TraSubOrder


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
    
    monthDetails = db.session.query(
        subq2.c.day,
        __model.rest_flg,
        db.func.to_char(db.func.sum(__model.work_time),'HH24:MI').label('workTime'),
    ).outerjoin(__model, 
        and_(
        subq2.c.day == __model.work_day,
        __model.user_id == userId,
        __model.work_year == year,
        __model.work_month == month
        )
    ).group_by(
        subq2.c.day,
        __model.rest_flg
    ).order_by(
        subq2.c.day
    ).all()

    return monthDetails

def selectTraClientWorkList(groupId, userId, year, month, day):
    """選択された日の稼働リストを取得するDB処理

    :param groupId: 登録ユーザの所属コード
    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
    orderCd = aliased(TraOrder)
    subOrderCd = aliased(TraSubOrder)

    clientWorkList = db.session.query( 
        __model.client_work_id.label('clientWorkId'),
        db.func.to_char(__model.work_time,'HH24:MI').label('workTime'),
        orderCd.order_value.label('orderCd'),
        __model.task_cd.label('taskCd'),
        func.COALESCE(subOrderCd.sub_order_value, 'なし').label('subOrderCd') 
        ).filter(
            __model.user_id == userId,
            __model.work_year == year,
            __model.work_month == month,
            __model.work_day == day,
            __model.rest_flg == 0
        ).outerjoin(
            (orderCd,
            and_(orderCd.order_cd == __model.order_cd,
            orderCd.group_id == groupId)),
            (subOrderCd,
            and_(subOrderCd.order_cd == __model.order_cd,
            subOrderCd.sub_order_cd == __model.sub_order_cd,
            subOrderCd.group_id == groupId))
        ).all()

    return clientWorkList

def selectTraClientWorkDetails(clientWorkId):
    """選択された稼働詳細を取得するDB処理

    :param clientWorkId: 稼働詳細ID
    """
    clientWorkDetails = db.session.query(
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
    return clientWorkDetails

def insertUpdateTraClientWork(dto,isUpdate):
    """稼働詳細の新規または修正を処理するDB処理

    :param dto: 稼働詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __model()
    model.user_id = dto['userId'],
    model.work_year = dto['year'],
    model.work_month = dto['month'],
    model.work_day = dto['day'],
    model.rest_flg = 0,
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

def insertDayOffFlg(userId, year, month, day):
    """選択された日を休みとして登録するDB処理

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
    model = __model()
    model.user_id = userId,
    model.work_year = year,
    model.work_month = month,
    model.work_day = day,
    model.rest_flg = 1,
    db.session.add(model)
    db.session.flush()

def deleteDay(userId, year, month, day, restFlg=1):
    """選択された日の稼働情報を削除するDB処理

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
    __model.query.filter_by(
        user_id = userId,
        work_year = year,
        work_month = month,
        work_day = day,
        rest_flg = restFlg
        ).delete()
    db.session.flush()

def deleteTraClientWork(clientWorkId):
    """稼働詳細を削除するDB処理

    :param clientWorkId: 稼働詳細ID
    """
    __model.query.filter_by(client_work_id = clientWorkId).delete()
    db.session.flush()