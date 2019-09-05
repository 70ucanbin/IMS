import openpyxl as px
import os, shutil
import traceback

class __ExcelUtil(object):
    def __init__(self, template_path, tmp_path):
        self.template_path = template_path
        self.tmp_path = tmp_path
        try:
            os.makedirs(tmp_path)
            self.tmp_file = shutil.copy(template_path, tmp_path+'\\旅費精算201909.xlsx')

            self.book = px.load_workbook(self.tmp_file)

        except:
            """ファイルを読み込み時のエラー処理を記述
            
            """
            if os.path.exists(tmp_path):
                shutil.rmtree(self.tmp_path)
            pass

    def edit_file(self):
        pass

    def close_file(self):
        try:
            self.book.close()
            shutil.rmtree(self.tmp_path)
        except:
            """ファイルを閉じる時のエラー処理を記述

            """
            traceback.print_exc()

class travelExpenses_excel(__ExcelUtil):
    
    def edit_file(self, models):
        try:

            if models:
                sheet = self.book.active
                row = 12
                column = 1
                for model in models:
                    sheet.cell(row, column).value = model.expense_date
                    sheet.cell(row, column+1).value = model.expense_item
                    sheet.cell(row, column+2).value = model.route
                    sheet.cell(row, column+4).value = model.transit
                    sheet.cell(row, column+5).value = model.payment
                    sheet.cell(row, column+6).value = ''
                    sheet.cell(row, column+7).value = model.attached_file_id
                    sheet.cell(row, column+8).value = model.note
            
            self.book.save(self.tmp_file)

            result_file = open(self.tmp_file, "rb").read()

        except TypeError:
            traceback.print_exc()

        super().close_file()

        return result_file
