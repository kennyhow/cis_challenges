import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluateasteroid():
    data = json.loads(request.data)['test_cases']
    def solve(s):
        def f(pos):
            ans = 1
            left_ptr, right_ptr = pos - 1, pos + 1
            while left_ptr >= 0 and right_ptr < len(s) and s[left_ptr] == s[right_ptr]:
                c = s[left_ptr]
                count = 2
                while left_ptr - 1 >= 0 and s[left_ptr - 1] == c:
                    left_ptr -= 1
                    count += 1
                while right_ptr + 1 < len(s) and s[right_ptr + 1] == c:
                    right_ptr += 1
                    count += 1
                left_ptr -= 1
                right_ptr += 1
                if count >= 10:
                    ans += 2 * count
                elif count >= 7:
                    ans += 1.5 * count
                else:
                    ans += count
            return ans
        best, pos = 0.0, 0
        for i in range(len(s)):
            res = f(i)
            if res > best:
                best = res
                pos = i
        return {"input": s, "score": best, "origin": pos}
    answer = list()
    for testcase in data:
        answer.append(solve(testcase))
    return json.dumps(answer)