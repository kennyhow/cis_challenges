import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/perry', methods=['POST'])
def evaluatestig1():
    data = json.loads(request.data)
    answer = list()
    for testcase in data:
        logging.info("question size {}".format(len(testcase['questions'])))
        logging.info("interval up to {}".format(testcase['maxRating']))
        answer.append({"p": 1, "q": 1})
    return json.dumps(answer)
