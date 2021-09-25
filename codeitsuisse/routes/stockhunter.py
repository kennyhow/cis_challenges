import logging
import json

from flask import request, jsonify
from queue import PriorityQueue

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stock-hunter', methods=['POST'])
def evaluatestockhunter():
    data = json.loads(request.data)
    final_answer = list()
    for testcase in data:
        a, b = testcase['entryPoint']['first'], testcase['entryPoint']['second']
        c, d = testcase['targetPoint']['first'], testcase['targetPoint']['second']
        depth = testcase['gridDepth']
        key = testcase['gridKey']
        horizontal = testcase['horizontalStepper']
        vertical = testcase['verticalStepper']
        risk_index = [[0 for _ in range(d + 1)] for _ in range(c + 1)]
        risk_level = risk_index[::]
        for i in range(c + 1):
            for j in range(d + 1):
                if (i, j) in [(a, b), (c, d)]:
                    risk_index[i][j] = 0
                elif i == 0:
                    risk_index[i][j] = j * horizontal
                elif j == 0:
                    risk_index[i][j] = i * vertical
                else:
                    risk_index[i][j] = risk_level[i - 1][j] * risk_level[i][j - 1]
                risk_level[i][j] = (risk_index[i][j] + depth) % key
        risk_cost = [[0 for _ in range(d + 1)] for _ in range(c + 1)]
        answer = [[0 for _ in range(d + 1)] for _ in range(c + 1)]
        for i in range(c + 1):
            for j in range(d + 1):
                if risk_level[i][j] % 3 == 0:
                    risk_cost[i][j] = 3
                    answer[i][j] = 'L'
                elif risk_level[i][j] % 3 == 1:
                    risk_cost[i][j] = 2
                    answer[i][j] = 'M'
                else:
                    risk_cost[i][j] = 1
                    answer[i][j] = 'S'
        
        distance = [[3 * (c + 2) * (d + 2) for _ in range(d + 1)] for _ in range(c + 1)]
        distance[0][0] = 0
        pp = PriorityQueue()
        pp.put((0, (0, 0)))
        while not pp.empty():
            x, y = pp.get()[1]
            nexts = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            current = distance[x][y]
            for p, q in nexts:
                if p >= 0 and q >= 0 and p <= c and q <= d:
                    next_distance = distance[p][q]
                    if next_distance > risk_cost[p][q] + distance[x][y]:
                        distance[p][q] = risk_cost[p][q] + current
                        pp.put((distance[p][q], (p, q)))
        final_answer.append({"gridMap": answer, "minimumCost": distance[c][d]})
    return json.dumps(final_answer)