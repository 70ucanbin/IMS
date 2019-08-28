


def getTraClientWork():
    sql = """
        SELECT
            to_char(SUM(work_time), 'HH24:MI') as workTime
        FROM
            tra_client_work
        WHERE
            employee_id = :employeeId
        AND
            work_year = :workYear
        AND
            work_month = :workMonth
        AND
            work_day = :workDay
    """
    return sql

    # sql = getTraClientWork()
    # result = db.engine.execute(
    #     text(sql), 
    #     {'employeeId':employeeId,'workYear':year,'workMonth':month,'workDay':day}
    # ).first()
    # names = result
    # return names[0]