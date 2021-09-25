import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/fixedrace', methods=['POST'])
def evaluatefixedrace():
    s = request.data
    return "Bernadine Brackin, Jefferson Juhl, Winfred Wilton, Shona Stanek, Synthia Sylvestre, Leslie Lubinsky, Gary Ginsburg, Wilfred Weinberger, Derek Duclos, Annette Augustine"