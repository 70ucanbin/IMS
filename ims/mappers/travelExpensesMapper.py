from ims.mappers.models.traTravelExpenses import TraTravelExpenses as __modle


# 稼働日の稼働時間合計を取得
def selectTraTravelExpenses(employeeId, year, month):
    dto = __modle.query.filter_by(
        employee_id = employeeId,
        entry_year = year,
        entry_month = month
    ).all()

    return dto