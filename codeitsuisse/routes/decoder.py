import logging
import json
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/decoder', methods=['POST'])
def evaluatedecoder():
    temp = request.data
    data = json.loads(temp)
    printable = data['possible_values']
    n = data['num_slots']
    values = data['history']
    
    possible = list()
    def recurse(prefix, pos):
        if pos == n:
            possible.append(prefix[::])
        else:
            for c in printable:
                recurse(prefix + c, pos + 1)
    recurse('', 0)
    results = list()
    for x in possible:
        valid = True
        freq_x = {c: x.count(c) for c in printable}
        for history in values:
            prev = history['output_received']
            result = history['result']
            right_count = result // 10
            right_exact = result % 10
            # assume x is exactly correct, try to find a contradiction
            freq = {c: prev.count(c) for c in printable}
            freq_old = freq_x.copy()
            for i in range(n):
                if x[i] == prev[i]:
                    freq_old[x[i]] -= 1
                    freq[x[i]] -= 1
                    right_exact -= 1
            for c in printable:
                change = min(freq[c], freq_old[c])
                right_count -= change
                freq[c] -= change
                freq_old[c] -= change
            if right_exact != 0 or right_count != 0:
                valid = False
                break
        if valid:
            results.append(list(x))
    app.logger.info("results have length {}".format(len(results)))
    if len(results) == 0:
        return json.dumps({"answer": list(random.choice(possible))})
    return json.dumps({"answer": list(random.choice(results))})
            