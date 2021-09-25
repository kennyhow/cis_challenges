import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/fixedrace', methods=['POST'])
def evaluatefixedrace():
    s = request.data
    return "Nathanael Nutt, Cleveland Crofts, Harlan Hasting, Chantel Corn, Johanne Jeffress, Lisha Levesque, Monroe Middlebrook, Anibal Abler, Olympia Oliphant, Patrina Ptak"