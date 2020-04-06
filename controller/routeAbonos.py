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

def montoAbonado(cuotas, importe):
    return cuotas * importe

@app.route('/abonos/add', methods=['POST'])
def agregardabonos():
    try:
        _json = request.json
        print(_json)
        # deuda = int(_json['monto'])
        # _json
        _jsonResponse = {
                "deuda" : _json['deuda'],
                "cuotas": _json['cuotas'],
                "interes": _json['interes'],
                "ImporteCuotas" : _json['ImporteCuotas'],
                "idClient" : _json['idClient'],
                "cuotasPagadas": _json['cuotasPagadas'],
                "montoTotalAbonado" : montoAbonado(float(_json['cuotasPagadas']), float(_json['ImporteCuotas'])),
                "expand": False,
                "created_at": li_time
            }
        # id = mongo.db.creditos.insert(_jsonResponse)
        id = mongo.db.abonos.insert(_jsonResponse)
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

@app.route('/abonos/<id>')
def getAbonosOne(id):
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.abonos.find({'idClient': id})
    resp = dumps(user)
    return resp