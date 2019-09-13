import json 
import urllib.parse

from datetime import date, datetime

from flask import request, redirect, url_for, render_template, flash, session, Blueprint, jsonify, make_response
from werkzeug.utils import secure_filename

from config import PathConfig as path

from ims.views.com import login_required
from ims.common.Constants import Contract
from ims.contents.travelExpensesCont import TravelExpensesListCont as listCont
from ims.contents.travelExpensesCont import TravelExpensesDetailsCont as detailsCont
from ims.service.travelExpensesServ import getTravelExpensesList as getDtoList
from ims.service.travelExpensesServ import getTravelExpensesDetails as getDto
from ims.service.travelExpensesServ import insertUpdateTravelExpenses as insertUpdateDto
from ims.service.travelExpensesServ import deleteTravelExpenses as deleteDto
from ims.form.travelExpensesForm import TravelExpensesForm
from ims.common.ComboBoxUtil import getNumberList
from ims.common.ExcelLogicUtil import travelExpenses_excel as getFile

travelExpenses = Blueprint('travelExpenses', __name__)


@travelExpenses.route('/travel_expenses/<int:month>/list/', methods = ['GET'])
@login_required
def travel_expenses_list(month):
    """旅費精算一覧の初期表示   GETのrequestを受付
    ナビバーからのrequsetはディフォルトで当月を表示します。
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    
    :param month: 該当月のデータ取得用「月」
    """
    if not month:
        month=date.today().month
    else:
        try:
            date(date.today().year, month, date.today().day)
        except ValueError:
            return redirect(url_for('travelExpenses.travel_expenses_list', month=0))

    #月のselectBox値取得
    monthList = getNumberList(1,13,1)
    cont = listCont(month, monthList)

    return render_template('travel_expenses/travel-expenses-list.html', cont=cont)


@travelExpenses.route('/travel_expenses/list/getData', methods = ['POST'])
@login_required
def travel_expenses_post_data():
    """旅費精算一覧表示用データ取得   POSTのrequestを受付
    
    一覧画面から選択された月のデータを取得し、json形式でデータを返します。
    """
    user = 'k4111'
    year = date.today().year

    try:
        month = int(request.json['month'])
        models = getDtoList(user, year, month)

        dataset = []
        for model in models:
            data = {}
            data["travelExpensesId"] = model.travel_expenses_id
            data["expenseDate"] = model.expense_date
            data["expenseItem"] = model.expense_item
            data["route"] = model.route
            data["transit"] = model.transit
            data["payment"] = int(model.payment)
            data["uploadFile"] = model.attached_file_id
            dataset.append(data)
    except:
        pass
    return jsonify(dataset)


@travelExpenses.route('/travel_expenses/<int:month>/download/')
@login_required
def travel_expenses_report_download(month):
    """旅費精算帳票出力処理

    一覧画面から「詳細出力」を押下後、データを帳票に書き込み、返します。

    :param month: 出力したい「月」
    """
    user = 'k4111'
    year = date.today().year
    models = getDtoList(user, year, month)

    file_path = path.TRAVEL_EXPENSES_EXCEL_TEMPLATE
    tmp_path = path.TMP + user + datetime.now().strftime('%Y%m%d%H%M%S')
    # パーセントエンコード
    file_name = urllib.parse.quote(path.TRAVEL_EXPENSES_EXCEL_FILE_NAME)

    data = getFile(file_path, tmp_path)
    
    response = make_response()
    response.data = data.edit_file(models)
    response.headers['Content-Disposition'] = 'attachment; filename=' + '"' + file_name + '";filename*=UTF-8\'\'' + file_name
    response.mimetype = 'application/vnd.ms-excel'

    return response


@travelExpenses.route('/travel_expenses/<int:month>/create/')
@login_required
def travel_expenses_create(month):
    """旅費精算作成処理

    一覧画面から「新規作成」または「月日」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param month: 追加対象データの月
    """
    try:
        date(date.today().year, month, date.today().day)
    except ValueError:
        return redirect(url_for('travelExpenses.travel_expenses_list', month=0))
    form = TravelExpensesForm()
    cont = detailsCont(month, form)

    return render_template('travel_expenses/travel-expenses-details.html', cont=cont)



@travelExpenses.route('/travel_expenses/<int:travelExpensesId>/edit/')
@login_required
def travel_expenses_edit(travelExpensesId):
    """旅費精算修正処理

    一覧画面から「新規作成」または「月日」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param travelExpensesId: 追加または修正対象データのIDです。
    """
    dto = getDto(travelExpensesId)
    if not dto:
        flash("指定されたデータは存在しません。他のユーザにより変更・削除されていないか確認してください。", 
            "list-group-item list-group-item-warning")
        return redirect(url_for('travelExpenses.travel_expenses_list', month=0))

    form = TravelExpensesForm()
    form.travelExpensesId.data = dto.travel_expenses_id
    form.expenseDate.data = dto.expense_date
    form.expenseItem.data = dto.expense_item
    form.route.data = dto.route
    form.transit.data = dto.transit
    form.payment.data = dto.payment
    form.note.data = dto.note
    form.uploadFile.data = dto.file_name

    cont = detailsCont(dto.entry_month, form)

    return render_template('travel_expenses/travel-expenses-details.html', cont=cont)


@travelExpenses.route('/details/<int:travelExpensesId>/downloadFile')
@login_required
def travel_expenses_file_download(travelExpensesId):

    dto = getDto(travelExpensesId)

    directory = "tmp\\"

    response = make_response()
    response.data = open(directory + dto.attached_file_id, "rb").read()

    downloadFileName = dto.attached_file_id
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName
    response.mimetype = 'application/vnd.ms-excel'

    return response


@travelExpenses.route('/travel_expenses/details/<int:month>', methods=['POST'])
@login_required
def travel_expenses_save(month):
    """旅費精算詳細画面確定処理

    formのデータをDBに保存します。
    処理終了後は旅費精算一覧画面へ遷移します。

    :param month: 一覧画面へ戻るときに遷移前の月を渡します。
    """
    # form = request.form.to_dict()
    # form['user_id'] = 'k4111'
    # form['year'] = date.today().year
    # form['month'] = month
    # payment = request.form['payment']
    # form['payment'] = int(payment.replace(',', ''))

    form = TravelExpensesForm()
    if form.validate_on_submit():
        print(request.data)
        data = form.data
        data['userId'] = 'k4111'
        data['entryYear'] = date.today().year
        data['entryMonth'] = month
        data['payment'] = int(data['payment'].replace(',', ''))

        if form.uploadFile.data:
            
            f = form.uploadFile.data

            file_path = path.TRAVEL_EXPENSES_UPLOAD_FILE_PATH
            filename = f.filename
            data['uploadFile'] = filename
            f.save(file_path + filename)

        if form.travelExpensesId.data:
            isUpdate = True
        else:
            isUpdate = False
        result = insertUpdateDto(data, isUpdate)
        if result and result['success'] == False:
            flash(result['message'], "list-group-item list-group-item-warning")
        return redirect(url_for('travelExpenses.travel_expenses_list', month=month))

    for error in form.errors.values():
        flash(error[0],"list-group-item list-group-item-danger")

    cont = detailsCont(month, form)

    return render_template('travel_expenses/travel-expenses-details.html', cont=cont)


@travelExpenses.route('/details/<int:month>/<int:travelExpensesId>/delete')
@login_required
def travel_expenses_delete(month, travelExpensesId):








    deleteDto(travelExpensesId)

    return redirect(url_for('travelExpenses.travel_expenses_list', month=month))