import traceback

from flask import abort
from sqlalchemy import exc

from ims import db
from ims.service.mappers.clientWorkMapper import selectTraClientWorkMonthList as __testgetWorkTime
from ims.service.mappers.clientWorkMapper import selectTraClientWork as __getWorkTime
from ims.service.mappers.clientWorkMapper import selectTraClientWorkList as __getList
from ims.service.mappers.clientWorkMapper import selectTraClientWorkDetails as __getDetails
from ims.service.mappers.clientWorkMapper import insertUpdateTraClientWork as __insertUpdateOne
from ims.service.mappers.clientWorkMapper import deleteTraClientWork as __deleteOne


# その月の稼働時間合計値
def getClientWorkMonthList(userId, year, month):
    result = __testgetWorkTime(userId, year, month)

    return result

# その日の稼働時間合計値
def getClientWork(userId, year, month, day):
    result = __getWorkTime(userId, year, month ,day)

    return result

def getClientWorkList(userId, year, month, day):
    dto = __getList(userId, year, month ,day)

    return dto

def getClientWorkDetails(clientWorkId):
    dto = __getDetails(clientWorkId)

    return dto

def insertUpdateClientWork(dto, isUpdate):
    try:
        result = __insertUpdateOne(dto,isUpdate)
        if result['success'] == True:
            db.session.commit()
            return result
        else:
            return result
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(404)
    finally: 
        db.session.close()


def deleteClientWork(clientWorkId):
    # try:
        result = __deleteOne(clientWorkId)
        # if result['success'] == True:
        db.session.commit()
    #         return result
    #     else:
    # except Exception:
    #     traceback.print_exc()
    #     db.session.rollback()
    #     abort(404)
    # finally: 
        db.session.close()
        return result