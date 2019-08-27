from ims.mappers.models.traClientWork import TraClientWork
from ims.mappers.sql.clientWorkSql import getTraClientWork
from ims import db
from sqlalchemy import text, select, literal_column, table
from sqlalchemy.sql import func
import json
from datetime import time

# def testsql():
#         json_object = json.loads(getsql())
#         textsql = json_object['testsql']
#         sql = text(textsql)
#         sqlin = 't or 1 = 1; delete from com_item'
#         result = db.engine.execute(sql,{'val':sqlin})

#         names = [row[0] for row in result]
#         print(names)

def selectTraClientWork(employeeId, year, month, day):
    sql = getTraClientWork()
    result = db.engine.execute(
        text(sql), 
        {'employeeId':employeeId,'workYear':year,'workMonth':month,'workDay':day}
    ).first()
    names = result
    # if names[0] == None:
    #     names[0] = ''
    return names[0]

