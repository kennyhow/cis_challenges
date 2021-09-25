import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/perry', methods=['POST'])
def evaluatestig1():
    def solve(testcase, maximum):
        intervals = testcase['questions']
        points = list()
        for interval in intervals:
            interval = interval[0]
            a, b = interval['from'], interval['to']
            points.append((a, b))
        points.sort(key = lambda point: point[0])

        total_intervals = list()
        left, right = -1, -1
        for i in range(len(points)):
            p, q = points[i]
            if left == -1 and right == -1:
                left, right = p, q
            elif p > right:
                total_intervals.append(left, right)
                left, right = p, q
            else:
                right = max(right, q)
        total_intervals.append((left, right))
        ans = maximum
        for p, q in total_intervals:
            ans -= (q - p + 1)
        return ans

    data = json.loads(request.data)
    logging.info(data)
    answer = list()
    for testcase in data:
        answer.append({"p": 1, "q": solve(testcase, testcase['maxRating'])})
    return json.dumps(answer)