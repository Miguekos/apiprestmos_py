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
    resultado = (monto * (porcent / 100)) + monto
    print(resultado)
    return resultado

def importePorCuotas(deuda, cuotas):
    return deuda / cuotas

@app.route('/creditos/add/<id>', methods=['POST'])
def agregardCreditos(id):
    try:
        _json = request.json
        print(_json)
        deudaTotal = calcuarDeuda(float(_json['monto']), float(_json['interes']))
        # _json
        _jsonResponse = {
                "deuda" : deudaTotal,
                "cuotas": _json['cuotas'],
                "ImporteCuotas" : importePorCuotas(deudaTotal, _json['cuotas']),
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

@app.route('/creditos/cronograma/<id>')
def getCrediCronogramaOne(id):
    print("Consultando Creditos del ID: {}".format(id))
    user = mongo.db.creditos.find({'idClient': id})
    abonos = mongo.db.abonos.find({'idClient': id})
    """
    Se trae la fecha en qeue se creo el credito se suma la cantidad de cuotas pagadas y asi calcular los dias restante 
    
    """
    for x in user:
        print(x['deuda'])
        print(x['created_at'])
        for b in abonos:
            print(b['montoTotalAbonado'])
            print(b['cuotasPagadas'])
            print(b['created_at'])
            # print(user)
            jsonResponse = {
                # deudaTotal
            }
    resp = dumps(user)
    return resp