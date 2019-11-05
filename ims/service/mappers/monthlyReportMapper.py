from ims import db
from ims.service.mappers.models.traMonthlyReport import TraMonthlyReport as __model


def selectTraMonthlyReportList(userId, year, month, day):
    """1ヶ月分旅費精算リストを取得するDB処理

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    """
    travelExpensesList = __model.query.filter_by(
        user_id = userId,
        entry_year = year,
        entry_month = month
    ).all()

    return travelExpensesList