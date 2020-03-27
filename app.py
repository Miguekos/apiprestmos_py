from flask import Flask

app = Flask(__name__)


import controller.routeUsers
import controller.routeCliente
import controller.routeCreditos