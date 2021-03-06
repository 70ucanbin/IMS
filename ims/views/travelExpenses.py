import os
import urllib.parse

from datetime import date, datetime

from flask import  Blueprint, flash, jsonify, make_response, request, redirect, render_template, url_for
from flask_login import login_required, current_user

from ims.common.AppPath import PathConfig as path
from ims.common.ComboBoxUtil import getNumberList, getUserList
from ims.common.ExcelLogicUtil import travelExpenses_excel as getFile
from ims.common.Messages import Messages
from ims.contents.travelExpensesCont import TravelExpensesListCont as listCont
from ims.contents.travelExpensesCont import TravelExpensesDetailsCont as detailsCont
from ims.form.travelExpensesForm import TravelExpensesForm
from ims.service.travelExpensesServ import getTravelExpensesList as getDtoList
from ims.service.travelExpensesServ import getTravelExpensesDetails as getDto
from ims.service.travelExpensesServ import insertUpdateTravelExpenses as insertUpdateDto
from ims.service.travelExpensesServ import deleteTravelExpenses as deleteDto

travelExpenses = Blueprint('travelExpenses', __name__)


@travelExpenses.route('/<int:month>/list/')
@login_required
def travel_expenses_list(month):
    """旅費精算一覧の初期表示  GETのrequestを受付
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
    # 月のselectBox値取得
    monthList = getNumberList(1,13,1)
    # ユーザのselectBox値取得
    cont = listCont(month, monthList)
    if current_user.role == 2:
        cont.userList = getUserList(current_user.group_id)

    return render_template('travel_expenses/travel-expenses-list.html', cont=cont)


@travelExpenses.route('/list/getData/', methods = ['POST'])
@login_required
def travel_expenses_post_data():
    """旅費精算一覧表示用データ取得  POSTのrequestを受付

    一覧画面から選択された月のデータを取得し、json形式でデータを返します。
    """
    year = date.today().year

    try:
        month = int(request.json['month'])
        
        if current_user.role == 2:
            userId = request.json['userId']
            models = getDtoList(userId, year, month)
        else:
            models = getDtoList(current_user.user_id, year, month)
        dataset = []
        for model in models:
            data = {}
            data["travelExpensesId"] = model.travel_expenses_id
            data["expenseDate"] = model.expense_date
            data["expenseItem"] = model.expense_item
            data["route"] = model.route
            data["transit"] = model.transit
            data["payment"] = int(model.payment)
            data["uploadFile"] = model.file_name
            dataset.append(data)
    except:
        pass
    return jsonify(dataset)


@travelExpenses.route('/<int:month>/<string:userId>/download/')
@login_required
def travel_expenses_report_download(month, userId):
    """旅費精算帳票出力処理

    一覧画面から「詳細出力」を押下後、データを帳票に書き込み、返します。

    :param month: 出力したい「月」
    """
    year = date.today().year
    if current_user.role == 2:
        models = getDtoList(userId, year, month)
    else:
        models = getDtoList(current_user.user_id, year, month)

    if not models:
        flash(Messages.NO_DATA_AVAILABLE, Messages.WARNING_CSS)
        return redirect(url_for('travelExpenses.travel_expenses_list', month=month))

    templatePath = path.TRAVEL_EXPENSES_EXCEL_TEMPLATE
    tmpPath = path.TMP + current_user.user_id + datetime.now().strftime('%Y%m%d%H%M%S')
    # パーセントエンコード
    fileName = urllib.parse.quote(path.TRAVEL_EXPENSES_EXCEL_FILE_NAME)

    # Excel処理
    fileData = getFile(templatePath, tmpPath)

    # レスポンス作成
    response = make_response()
    response.data = fileData.edit_file(userId, models)
    response.headers['Content-Disposition'] = 'attachment; filename=' + '"' + fileName + '";filename*=UTF-8\'\'' + fileName
    response.mimetype = 'application/vnd.ms-excel'

    return response


@travelExpenses.route('/<int:month>/create/')
@login_required
def travel_expenses_create(month):
    """旅費精算作成処理

    一覧画面から「新規作成」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param month: 追加対象データの月
    """
    try:
        date(date.today().year, month, date.today().day)
    except ValueError:
        return redirect(url_for('travelExpenses.travel_expenses_list', month=0))

    cont = detailsCont(month, TravelExpensesForm())
    cont.is_self = True
    return render_template('travel_expenses/travel-expenses-details.html', cont=cont)



@travelExpenses.route('/<int:travelExpensesId>/edit/')
@login_required
def travel_expenses_edit(travelExpensesId):
    """旅費精算修正処理

    一覧画面から「月日」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param travelExpensesId: 修正対象データのID
    """
    dto = getDto(travelExpensesId)
    if not dto:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('travelExpenses.travel_expenses_list', month=0))

    cont = detailsCont()
    cont.month = dto.entry_month
    if dto.user_id == current_user.user_id:
        cont.is_self = True

    form = TravelExpensesForm()
    form.travelExpensesId.data = dto.travel_expenses_id
    form.expenseDate.data = dto.expense_date
    form.expenseItem.data = dto.expense_item
    form.route.data = dto.route
    form.transit.data = dto.transit
    form.payment.data = dto.payment
    form.note.data = dto.note
    form.uploadFile.data = dto.file_name

    cont.form = form

    return render_template('travel_expenses/travel-expenses-details.html', cont=cont)


@travelExpenses.route('/details/<int:travelExpensesId>/downloadFile/')
@login_required
def travel_expenses_file_download(travelExpensesId):
    """旅費精算詳細画面添付ファイルダウンロード処理

    :param travelExpensesId: 該当データのID。
    """
    dto = getDto(travelExpensesId)

    directory = path.TRAVEL_EXPENSES_UPLOAD_FILE_PATH + str(date.today().year) + "\\"
    directory = directory + str(dto.entry_month) + "\\" + dto.user_id + "\\"

    response = make_response()
    response.data = open(directory + dto.file_name, "rb").read()
    response.headers['Content-Disposition'] = 'attachment; filename=' + dto.file_name
    response.mimetype = 'application/vnd.ms-excel'

    return response


@travelExpenses.route('/details/<int:month>/save/', methods=['POST'])
@login_required
def travel_expenses_save(month):
    """旅費精算詳細画面登録処理

    formのデータをDBに保存します。
    処理終了後は旅費精算一覧画面へ遷移します。

    :param month: 一覧画面へ戻るときに遷移前の月を渡します。
    """
    form = TravelExpensesForm()
    if form.validate_on_submit():
        # (新規・修正)判定
        dto = getDto(form.travelExpensesId.data)
        if form.travelExpensesId.data:
            isUpdate = True
            if dto and dto.user_id == current_user.user_id:
                pass
            else:
                flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
                    Messages.WARNING_CSS)
                return redirect(url_for('travelExpenses.travel_expenses_list', month=0))
        else:
            isUpdate = False

        data = form.data
        data['userId'] = current_user.user_id
        data['entryYear'] = date.today().year
        data['entryMonth'] = month
        data['payment'] = int(data['payment'].replace(',', ''))

        # 添付ファイル処理
        if form.uploadFile.data:
            data['uploadFile'] = form.uploadFile.data.filename
            directory = path.TRAVEL_EXPENSES_UPLOAD_FILE_PATH + str(date.today().year) + "\\"
            directory = directory + str(month) + "\\" + current_user.user_id + "\\"

            if os.path.exists(directory):
                pass
            else:
                os.makedirs(directory)
            if dto:
                if dto.file_name and isUpdate:
                    os.remove(directory + dto.file_name)
            form.uploadFile.data.save(directory + form.uploadFile.data.filename)
        else:
            data['uploadFile'] = form.uploadFile.data.filename
        insertUpdateDto(data, isUpdate)
        if isUpdate:
            flash(Messages.SUCCESS_UPDATED, Messages.SUCCESS_CSS)
        else:
            flash(Messages.SUCCESS_INSERTED, Messages.SUCCESS_CSS)
        return redirect(url_for('travelExpenses.travel_expenses_list', month=month))

    for error in form.errors.values():
        flash(error[0], Messages.DANGER_CSS)

    cont = detailsCont(month, form)

    return render_template('travel_expenses/travel-expenses-details.html', cont=cont)


@travelExpenses.route('/details/<int:month>/<int:travelExpensesId>/delete/')
@login_required
def travel_expenses_delete(month, travelExpensesId):
    """旅費精算詳細画面削除処理

    当該データを物理削除します。
    処理終了後は旅費精算一覧画面へ遷移します。

    :param month: 一覧画面へ戻るときに遷移前の月を渡します。
    :param travelExpensesId: 削除対象のIDです。
    """
    dto = getDto(travelExpensesId)
    if dto and dto.user_id == current_user.user_id:
        pass
    else:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('travelExpenses.travel_expenses_list', month=0))

    deleteDto(travelExpensesId)
    flash(Messages.SUCCESS_DELETED, Messages.SUCCESS_CSS)
    return redirect(url_for('travelExpenses.travel_expenses_list', month=month))