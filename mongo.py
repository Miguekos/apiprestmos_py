from app import app
from flask_pymongo import PyMongo

app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://144.217.14.34:27017/prestamos"
mongo = PyMongo(app)