from ims.mappers.travelExpensesMapper import selectTraTravelExpensesList as __getList
from ims import db
from flask import abort
from sqlalchemy import exc
import traceback

def getTravelExpensesList(employeeId, year, month):
    dto = __getList(employeeId, year, month)

    return dto
