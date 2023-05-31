from flask import Flask

app = Flask(__name__,instance_relative_config=True)

app.config.from_object("config")

ORIGIN_DATA = "data/cripto.sqlite"

from opera_cripto.routes import *