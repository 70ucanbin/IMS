
def selectClientWorkJoinCom():
    sql =   """
            SELECT
                client_work_id                         as clientWorkId
                , to_char(work_time, 'HH24:MI')        as workTime
                , S01.item_value                       as orderCd
                , S02.item_value                       as taskCd
                , S03.item_value                       as subOrderCd
            FROM
                tra_client_work as tcw
                LEFT JOIN com_item S01
                ON tcw.order_cd                         = S01.item_key
                AND S01.item_category                    = '1'
                LEFT JOIN com_item S02
                ON tcw.task_cd                          = S02.item_key
                AND S02.item_category                    = '3'
                LEFT JOIN com_item S03
                ON tcw.sub_order_cd                     = S03.item_key
                AND S03.item_category                    = '2'
            WHERE
                tcw.employee_id = :employeeId
            AND
                tcw.work_year = :workYear
            AND
                tcw.work_month = :workMonth
            AND
                tcw.work_day = :workDay
            """
    return sql

    # sql = getTraClientWork()
    # result = db.engine.execute(
    #     text(sql), 
    #     {'employeeId':employeeId,'workYear':year,'workMonth':month,'workDay':day}
    # ).first()
    # names = result
    # return names[0]