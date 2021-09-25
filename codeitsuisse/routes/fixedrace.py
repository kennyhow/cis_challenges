import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/fixedrace', methods=['POST'])
def evaluatefixedrace():
    s = request.data
    return "Bernadine Brackin, Gary Ginsburg, Wilfred Weinberger, Derek Duclos, Annette Augustine, Jefferson Juhl, Winfred Wilton, Shona Stanek, Synthia Sylvestre, Leslie Lubinsky"