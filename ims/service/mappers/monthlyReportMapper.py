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
    travelExpensesList = __model.query.filter_by(
        user_id = userId,
        entry_year = year,
        entry_month = month
    ).all()

    return travelExpensesList