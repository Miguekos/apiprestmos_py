from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
from bson.json_util import dumps, loads
# JSON.parse (dumps)
from bson.objectid import ObjectId
from flask_cors import CORS
from datetime import datetime, timedelta
from main import timestamp, li_time
import pytz
import funciones
CORS(app, supports_credentials=True)

def calcuarDeuda(monto, porcent):
    resultado = (monto * (porcent / 100)) + monto
    print(resultado)
    return resultado

def importePorCuotas(deuda, cuotas):
    return deuda / cuotas

def sumalista(listaNumeros):
    laSuma = 0
    for i in listaNumeros:
        laSuma = laSuma + i
    return laSuma


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
                "activo": True,
                "estado": True,
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
    creditos = mongo.db.creditos.find({'idClient': id})
    # creditos = mongo.db.alertas.insert({
    #     'idClient': id,
    #     'idCredit': id
    #             })
    resp = dumps(creditos)
    asd = loads(resp)
    cantidadCreditos = len(asd)
    for x in asd:
        print(x['idClient'])
    print(cantidadCreditos)
    # print(resp)
    return resp

@app.route('/creditos/cronograma/<id>')
def getCrediCronogramaOne(id):
    print("Consultando Creditos del ID: {}".format(id))
    abonos = mongo.db.abonos.find({'idCredito': id})
    print(abonos)
    """
    Se trae la fecha en qeue se creo el credito se suma la cantidad de cuotas pagadas y asi calcular los dias restante 
    """
    global Total
    global montoTotalAbonado
    global cuotasPagadas
    montoTotalAbonado = []
    Total = []
    cuotasPagadas = []
    credit = mongo.db.creditos.find({'_id': ObjectId(id)})
    for x in credit:
        print(x)
        global deudaCredito, fechaIniCredito, cuotasCredito, clienteId
        clienteId = x['_id']
        print("clienteId", clienteId)
        deudaCredito = x['deuda']
        fechaIniCredito = x['created_at'] - timedelta(hours=5)
        # print("fechaIniCredito", fechaIniCredito)
        cuotasCredito = x['cuotas']
        # print(deudaCredito)
    for b in abonos:
        # idDelCliente = b['idClient']
        # credit = mongo.db.creditos.find({'idClient': idDelCliente}, {'_id': ObjectId(id)})
        # print(fechaIniCredito)
        montos = b['montoTotalAbonado']
        cuotas = b['cuotasPagadas']
        fechas = b['created_at'] - timedelta(hours=5)
        # print(type(fechas))
        # print(fechas)
        # fechas = b['created_at'] - timedelta(days=30)
        # print("fechas", datetime("{}".format(fechas), tzinfo=pytz.timezone('Asia/Shanghai')))
        montoTotalAbonado.append(montos)
        cuotasPagadas.append(cuotas)
        jsonResponse = {
            "montoAbonado" : montos,
            "cuotasPagadas" : cuotas,
            "fechaIngreso" : "{}".format(fechas)
        }
        Total.append(jsonResponse)
    sumaAbonos = sumalista(montoTotalAbonado)
    sumaCuotas = sumalista(cuotasPagadas)
    primaFechaDePAgo = funciones.noSunday(fechaIniCredito, 29, cuotasCredito - sumaCuotas)
    cuotasPorPagarVar = cuotasCredito - sumaCuotas
    if cuotasPorPagarVar == 0:
        print("actuaizar estado")
        mongo.db.creditos.update_one({'_id': ObjectId(clienteId)},
                                 {'$set': {'estado': False}})
    else:
        mongo.db.creditos.update_one({'_id': ObjectId(clienteId)},
                                     {'$set': {'estado': True}})
        print("no pasa nada")
    _jsonResult = {
        "deuda" : deudaCredito,
        "deudaActual" : deudaCredito - sumaAbonos,
        "fechaInicioCredito" : "{}".format(fechaIniCredito),
        "pagos" : Total,
        "totalAbonado" : sumaAbonos,
        "totalCuotasPagadas" : sumaCuotas,
        "cuotasPorPagar" : cuotasPorPagarVar,
        "proximadiadepago" : primaFechaDePAgo['fechasCuotas'],
        "DiasMora": primaFechaDePAgo['DiasVencidos'] + 1
    }
    resp = dumps(_jsonResult)
    return resp