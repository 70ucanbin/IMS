from flask import request, redirect, url_for, render_template, flash, session, Blueprint, jsonify
from flask_login import login_required
import json, requests

api = Blueprint('api', __name__)

@api.route('/list', methods = ['GET','POST'])
def testapi():
    if request.method == 'GET':
        return render_template('api.html')
    elif request.method == 'POST':
        name = request.json["tenmei"]
        if name:
            keyid = 'c5f82059feb806a787833dba50f99a65'
            url = "https://api.gnavi.co.jp/RestSearchAPI/v3/?keyid=" + keyid + '&' + 'name=' +name
            headers = {'content-type': 'application/json'}
            r = requests.get(url, headers=headers)
            print(r.status_code)
            data = r.json()
            dataset = data
            return jsonify(dataset)
        else:
            dataset = [{
                "id": "1",
                "name": "2019-08-22",
                "address": "System Architect",
                "station": "$3,120",
                "opentime": "Edinburgh"
            }]
            return jsonify(dataset)