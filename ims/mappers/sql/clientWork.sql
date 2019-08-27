{"testsql":
"   SELECT
        SUM(hours_of_work) as workTime
    FROM
        tra_client_work
    WHERE
        employee_id = :val
"
}