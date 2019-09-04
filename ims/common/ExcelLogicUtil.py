import openpyxl as px
import traceback

class __ExcelUtil(object):
    def __init__(self, file_path=None):
        self.file_path = file_path
        try:
            self.book = px.load_workbook(self.file_path)

        except:
            """ファイルを読み込み時のエラー処理を記述

            """
            pass

    def edit_file(self):
        pass

    def close_file(self):
        try:
            self.book.save(self.file_path)
            self.book.close()
        except:
            """ファイルを閉じる時のエラー処理を記述

            """
            traceback.print_exc()
class travelExpenses_excel(__ExcelUtil):
    
    def edit_file(self, models):
        try:

            sheet = self.book.active

            row = 12
            column = 1
            if models:
                for model in models:
                    sheet.cell(row, column).value = model.expense_date
                    sheet.cell(row, column+1).value = model.expense_item
                    sheet.cell(row, column+2).value = model.route
                    sheet.cell(row, column+4).value = model.transit
                    sheet.cell(row, column+5).value = model.payment
                    sheet.cell(row, column+6).value = ''
                    sheet.cell(row, column+7).value = model.attached_file_id
                    sheet.cell(row, column+8).value = model.note
        except TypeError:
            traceback.print_exc()

        super().close_file()

        return 'end'
