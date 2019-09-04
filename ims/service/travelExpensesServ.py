from ims.mappers.travelExpensesMapper import selectTraTravelExpenses as __getList
from ims import db
from flask import abort
from sqlalchemy import exc
import traceback

def getTravelExpenses(employeeId, year, month):
    dto = __getList(employeeId, year, month)

    return dto
