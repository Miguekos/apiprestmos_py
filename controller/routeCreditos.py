from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
from bson.json_util import dumps
# JSON.parse (dumps)
from bson.objectid import ObjectId
from flask_cors import CORS
from main import timestamp, li_time
CORS(app, supports_credentials=True)

def calcuarDeuda(monto, porcent):
    return monto * (porcent / 100) + monto

@app.route('/creditos/add/<id>', methods=['POST'])
def agregardCreditos(id):
    try:
        _json = request.json
        print(_json)
        deuda = int(_json['monto']) + 1200
        # _json
        _jsonResponse = {
                "deuda" : calcuarDeuda(deuda, _json['interes']),
                "cuotas": _json['cuotas'],
                "interes": _json['interes'],
                "idClient" : id,
                "expand": False,
                "created_at": li_time
            }
        id = mongo.db.creditos.insert(_jsonResponse)
        resp = jsonify('{}'.format(id))
        resp.status_code = 200
        return resp
        # print(_jsonResponse)
        # return _jsonResponse
    except ValueError:
        print(ValueError)
        # jsonResp = {
        #     "codRes": "99",
        #     "message": "{}".format("error controlado")
        # }
        # return jsonify(jsonResp)

@app.route('/creditos/<id>')
def getCrediOne(id):
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.creditos.find({'idClient': id})
    resp = dumps(user)
    return resp