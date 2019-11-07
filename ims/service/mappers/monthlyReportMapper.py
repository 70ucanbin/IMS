from sqlalchemy import and_, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError

from ims import db
from ims.service.mappers.models.traMonthlyReport import TraMonthlyReport as __model
from ims.service.mappers.models.comItem import ComItem


def selectMonthlyReportDetails(userId, year, month, startDay, endDay):
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
        __model.rest_flg,
        db.func.to_char(
            __model.normal_working_hours + __model.overtime_hours + __model.holiday_work_hours,
            '999D99'
            ).label('workTime'),
    ).outerjoin(__model, 
        and_(
        subq2.c.day == __model.work_day,
        __model.user_id == userId,
        __model.work_year == year,
        __model.work_month == month
        )
    ).order_by(
        subq2.c.day
    ).all()

    return workMonthDetails

def insertUpdateTraMonthlyReport(dto,isUpdate):
    """月報詳細の新規または修正を処理するDB処理
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 月報詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __model()
    model.user_id = dto['userId'],
    model.work_year = dto['year'],
    model.work_month = dto['month'],
    model.work_day = dto['day'],
    model.rest_flg = 0,
    model.start_work_time = dto['startWorkTime'],
    model.end_work_time = dto['endWorkTime'],
    model.normal_working_hours = dto['normalWorkingHours'] or 0,
    model.overtime_hours = dto['overtimeHours'] or 0,
    model.holiday_work_hours = dto['holidayWorkHours'] or 0,
    model.note = dto['note'] or ""

    if isUpdate:
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()