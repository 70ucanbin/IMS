from ims import db
from ims.mappers.models.traTravelExpenses import TraTravelExpenses as __modle
from sqlalchemy.types import Integer, String
from sqlalchemy.sql import func
import traceback


# 1月分旅費精算リストを取得
def selectTraTravelExpensesList(employeeId, year, month):
    travelExpensesList = __modle.query.filter_by(
        employee_id = employeeId,
        entry_year = year,
        entry_month = month
    ).all()

    return travelExpensesList

def selectTraTravelExpensesDetails(employeeId, year, month):
    travelExpenses = __modle.query.filter_by(
        employee_id = employeeId,
        entry_year = year,
        entry_month = month
    ).all()

    return travelExpenses