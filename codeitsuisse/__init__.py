from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.parasite
import codeitsuisse.routes.fixedrace
import codeitsuisse.routes.asteroid
import codeitsuisse.routes.decoder
import codeitsuisse.routes.stockhunter
import codeitsuisse.routes.stig
import codeitsuisse.routes.optopt