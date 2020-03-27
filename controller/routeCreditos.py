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

@app.route('/creditos/add/<id>/<dni>', methods=['POST'])
def agregardCreditos(id, dni):
    try:
        _json = request.json
        deuda = _json['monto'] + 1200
        _json.update(
            {
                "deuda" : deuda,
                "dni" : dni,
                "id" : id
            }
        )
        # _json
        print(_json)
        return _json
    except:
        return "ok"

@app.route('/creditos', methods=['POST'])
def agregardCreditos(id, dni):
    if request.method == 'POST':
        try:
            _json = request.json
            deuda = _json['monto'] + 1200
            _json.update(
                {
                    "deuda" : deuda,
                    "dni" : dni,
                    "id" : id
                }
            )
            # _json
            print(_json)
            return _json
        except:
            return "ok"
    elif request.method == 'GET':
        return "soy get"