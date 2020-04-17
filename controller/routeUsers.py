from app import app
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from mongo import mongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS
CORS(app, supports_credentials=True)

# Rutas User
@app.route('/user/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']
    # validate the received values
    if _name and _email and _password and request.method == 'POST':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save details
        id = mongo.db.user.insert({'name': _name, 'email': _email, 'pwd': _hashed_password})
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/login', methods=["POST"])
def login():
    _json = request.json
    _user = mongo.db.user.find_one({
        'email': _json["email"]
    })
    validar = check_password_hash(_user['pwd'], _json["pwd"])
    if validar == True:
        idUser = _user['_id']
        print(idUser)
        jsonFinal = {
            "codRes": "00",
            "id" : idUser,
            "name" : _user['name'],
            "email": _user['email']
        }
        return dumps(jsonFinal)
    else:
        jsonFinal = {
            "codRes" : "01",
            "message" : "LoginIncorrecto"
        }
        resp = jsonify(jsonFinal)
        resp.status_code = 200
        return resp

@app.route('/user/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route('/user/update', methods=['PUT'])
def update_user():
    _json = request.json
    _id = _json['_id']
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']
    # validate the received values
    if _name and _email and _password and _id and request.method == 'PUT':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save edits
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                     {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
