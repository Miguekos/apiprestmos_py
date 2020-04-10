from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
from bson.json_util import dumps
# JSON.parse (dumps)
from bson.objectid import ObjectId
from flask_cors import CORS
from pytz import timezone
from datetime import datetime, timedelta
CORS(app, supports_credentials=True)

def montoAbonado(cuotas, importe):
    return cuotas * importe

@app.route('/abonos/add', methods=['POST'])
def agregardabonos():
    lima = timezone('America/Lima')
    li_time = datetime.now(lima)
    print("Rcibido el abnono", li_time)
    try:
        _json = request.json
        print(_json)
        # deuda = int(_json['monto'])
        # _json
        _jsonResponse = {
                "cliente": _json['cliente'],
                "dni": _json['dni'],
                "deuda" : _json['deuda'],
                "cuotas": _json['cuotas'],
                "interes": _json['interes'],
                "ImporteCuotas" : _json['ImporteCuotas'],
                "idClient" : _json['idClient'],
                "idCredito": _json['_id']['$oid'],
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


@app.route('/abonos')
def getAbonos():
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.abonos.find()
    resp = dumps(user)
    return resp

@app.route('/abonos/<id>')
def getAbonosOne(id):
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.abonos.find({'idClient': id})
    resp = dumps(user)
    return resp

@app.route('/abonos/delete/<id>', methods=['DELETE'])
def deleteAbonosOne(id):
    print("Consultando Creditos del ID: {}".format(id))
    mongo.db.abonos.delete_one({'_id': ObjectId(id)})
    resp = jsonify('abono eliminado correctamente!')
    resp.status_code = 200
    return resp

