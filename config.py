class AppConfig(object):
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@192.168.1.7/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # app configuration
    DEBUG = True
    SECRET_KEY = 'secret key'
    USERNAME = 'yo'
    PASSWORD = 'yoyoyo'

class PathConfig():
    # tmp path
    TMP = "tmp\\"

    # client work
    CLIENT_WORK_EXCEL_TEMPLATE = 'ims\\contents\\excelTemplate\\clientWork.xlsx'
    CLIENT_WORK_UPLOAD_FILE_PATH = 'D:\\tmp\\稼働情報'

    MONTHLY_REPORT_EXCEL_TEMPLATE = 'ims\\contents\\excelTemplate\\monthlyReport.xlsx'
    MONTHLY_REPORT_UPLOAD_FILE_PATH = 'D:\\tmp\\月報'

    TRAVEL_EXPENSES_EXCEL_TEMPLATE = 'ims\\contents\\excelTemplate\\travelExpenses.xlsx'
    TRAVEL_EXPENSES_UPLOAD_FILE_PATH = 'D:\\tmp\\旅費精算領収書\\'
    TRAVEL_EXPENSES_EXCEL_FILE_NAME = '旅費精算領収書.xlsx'

class Messages():
    SUCCESS_INSERTED = 'データを作成しました。'
    SUCCESS_UPDATED = 'データを更新しました。'
    SUCCESS_DELETED = '指定されたデータを削除しました。'
    WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED = '指定されたデータは存在しません。他のユーザにより変更・削除されていないか確認してください。'