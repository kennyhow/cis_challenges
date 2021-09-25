import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])

def evaluateparasite():
    def split_point(point):
        point = point.split(',')
        return tuple(map(int, point))

    def first_solve(start, end, grid):
        points = [start]
        visited = [[False for _ in range(m)] for _ in range(n)]
        visited[start[0]][start[1]] = True
        ans = 0
        while len(points) > 0 and end not in points:
            next_points = list()
            for x, y in points:
                # can move across 1 and 3 only
                nexts = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for p, q in nexts:
                    if p >= 0 and p < n and q >= 0 and q < m and grid[p][q] in [1, 3] and visited[p][q] == False:
                        visited[p][q] = True
                        next_points.append((p, q))
            ans += 1
            points = next_points[::]
        if end in points:
            return ans
        else:
            return -1

    def second_solve(start, grid):
        points = [start]
        ans = 0
        count = 0
        for i in range(n):
            for j in range(m):
                count += (grid[i][j] == 1)
        visited = [[False for _ in range(m)] for _ in range(n)]
        while len(points) > 0 and count > 0:
            next_points = list()
            for x, y in points:
                nexts = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for p, q in nexts:
                    if p >= 0 and p < n and q >= 0 and q < m and grid[p][q] == 1 and visited[p][q] == False:
                        visited[p][q] = True
                        next_points.append((p, q))
                        count -= 1
            ans += 1
            points = next_points[::]
        if count == 0:
            return ans
        else:
            return -1

        
    def third_solve(start, grid):
        points = [start]
        ans = 0
        count = 0
        for i in range(n):
            for j in range(m):
                count += (grid[i][j] == 1)
        visited = [[False for _ in range(m)] for _ in range(n)]
        while len(points) > 0 and count > 0:
            next_points = list()
            for x, y in points:
                nexts = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
                for p, q in nexts:
                    if p >= 0 and p < n and q >= 0 and q < m and grid[p][q] == 1 and visited[p][q] == False:
                        visited[p][q] = True
                        next_points.append((p, q))
                        count -= 1
            ans += 1
            points = next_points[::]
        if count == 0:
            return ans
        else:
            return -1
    input = json.loads(request.data)
    answer = list()
    for testcase in input:
        grid = testcase['grid']
        room = testcase['room']
        n, m = len(grid), len(grid[0])
        points = testcase['interestedIndividuals']
        prev_point = points[::]
        for i in range(len(points)):
            points[i] = split_point(points[i])
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 3:
                    start = (i, j)
        first_res = {}
        for i, point in enumerate(points):
            first_res[prev_point[i]] = first_solve(start, point, grid)
        output = {"room": room, "p1": first_res, "p2": second_solve(start, grid), "p3": third_solve(start, grid), "p4" : 0}
        answer.append(output)
    return json.dumps(answer)