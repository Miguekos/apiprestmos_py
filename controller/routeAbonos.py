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
import collections
CORS(app, supports_credentials=True)

def montoAbonado(tipo, cuotasMonto, cuotas, importe):
    print("cuotasMonto: ", cuotasMonto)
    print("cuotasMontoType: ", type(cuotasMonto))
    if tipo == 1:
        return cuotas * importe
    elif tipo == 2:
        return float(cuotasMonto)

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
        montoTotalAbonado = montoAbonado(_json['tipoPago'],_json['cuotasMonto'], float(_json['cuotasPagadas']), float(_json['ImporteCuotas']))
        _jsonResponse = {
                "cliente": _json['cliente'],
                "dni": _json['dni'],
                "deuda" : _json['deuda'],
                "cuotas": _json['cuotas'],
                "interes": _json['interes'],
                "ImporteCuotas" : _json['ImporteCuotas'],
                "idClient" : _json['idClient'],
                "idCredito": _json['_id']['$oid'],
                "tipoPago": _json['tipoPago'],
                "cuotasPagadas": _json['cuotasPagadas'],
                "montoTotalAbonado" : montoTotalAbonado,
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
    # print(list(user))
    # print(user)
    resp = dumps(user)
    # Converting string to list
    # res = resp.strip('][').split(', ')
    # # printing final result and its type
    # print("final list", res)
    # print(type(res))
    # print(type(user))
    # asd = collections.Counter(res)
    # print(asd)
    return resp

@app.route('/abonos/reporte')
def getAbonosReporte():
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.abonos.find()
    # print(user.next())
    # print(user.next())
    # print(user.next())

    #
    # user.rewind()
    #
    # print(user.next())
    # print(user.next())
    # print(user.next())
    # print(user.next()['_id'])
    # agr = [{'$group': {'_id': '$idClient'}}]
    agr = [
        {'$group': {'_id': '$idClient', 'pagos': {'$push':"$$ROOT"}}},
        {'$addFields':
            {
                'TotalAbonado': { '$sum' : "$pagos.montoTotalAbonado"}
            }
        },
        ]

    val = list(mongo.db.abonos.aggregate(agr))
    print(val)

    # print(list(user))


    # print(user)
    resp = dumps(user)
    # Converting string to list
    res = resp.strip('][').split(', ')
    # # printing final result and its type
    # print("final list", res)
    # print(type(res))
    # print(type(user))
    asd = collections.Counter(res)
    # print(asd)
    return dumps(val)

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

