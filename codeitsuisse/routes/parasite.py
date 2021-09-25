import logging
import json

from flask import request, jsonify
from queue import PriorityQueue

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
    
    counter = 0
    def fourth_solve(start, grid):

        # horizontally and vertically, cost in crossing over 0 and 2

        global counter
        origin = [[-1 for _ in range(m)] for _ in range(n)]
        counter = 0
        grouped_points = list()

        def process(i, j):
            global counter
            current_group = [(i, j)]
            points = [(i, j)]
            origin[i][j] = counter
            while len(points) > 0:
                next_points = list()
                for (p, q) in points:
                    nexts = [(p - 1, q), (p + 1, q), (p, q - 1), (p, q + 1)]
                    for (x, y) in nexts:
                        if x >= 0 and y >= 0 and x < n and y < m \
                            and grid[x][y] in [1, 3] and origin[x][y] == -1:
                            next_points.append((x, y))
                            current_group.append((x, y))
                            origin[x][y] = counter
                points = next_points[::]
            counter += 1
            grouped_points.append(current_group)

        for i in range(n):
            for j in range(m):
                if grid[i][j] in [1, 3] and origin[i][j] == -1:
                    process(i, j)

        # there are (counter) groups

        distance = [[n + m for _ in range(counter)] for _ in range(counter)]  # distance between groups

        def process_2(current_origin, points):

            # determines the minimum distance from any cell in this group to any other cell

            current_distance = [[n + m + 3000 for _ in range(m)] for _ in
                                range(n)]
            for (x, y) in points:
                current_distance[x][y] = 0

            # 0-1 bfs is fine

            pp = PriorityQueue()
            for x in points:
                pp.put((0, x))

            while not pp.empty():
                (a, (x, y)) = pp.get()
                if -a != current_distance[x][y]:
                    continue
                nexts = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for (p, q) in nexts:
                    if p >= 0 and q >= 0 and p < n and q < m:
                        temp = current_distance[p][q]
                        cost = current_distance[x][y]
                        if grid[p][q] in [0, 2]:
                            if cost + 1 < temp:
                                current_distance[p][q] = cost + 1
                                pp.put((-current_distance[p][q], (p, q)))
                        else:
                            if cost < current_distance[p][q]:
                                current_distance[p][q] = cost
                                pp.put((-current_distance[p][q], (p, q)))

            for i in range(n):
                for j in range(m):
                    if origin[i][j] not in [-1, current_origin]:
                        p = current_origin
                        q = origin[i][j]
                        distance[p][q] = min(distance[p][q],
                                current_distance[i][j])
                        distance[q][p] = min(distance[q][p],
                                current_distance[i][j])

        for i in range(counter):
            distance[i][i] = 0
        for i in range(counter):
            process_2(i, grouped_points[i])

        # points now:

        points = list()  # contains {distance, (group_left, group_right)}
        for i in range(counter):
            for j in range(i + 1, counter):
                points.append((distance[i][j], (i, j)))
        points = sorted(points)
        rep = [i for i in range(counter)]
        size = [1 for _ in range(counter)]

        def get_rep(group):
            while rep[group] != rep[rep[group]]:
                rep[group] = get_rep(rep[group])
            return rep[group]

        def unite(group_p, group_q):
            p = get_rep(group_p)
            q = get_rep(group_q)
            if p != q:
                if size[p] > size[q]:
                    p, q = q, p
                size[q] += size[p]
                rep[p] = q

        ans = 0
        for i in range(len(points)):
            dist = points[i][0]
            (p, q) = points[i][1]
            if get_rep(p) != get_rep(q):
                ans += dist
                unite(p, q)
        return ans

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
        output = {"room": room, "p1": first_res, "p2": second_solve(start, grid), "p3": third_solve(start, grid), "p4" : fourth_solve(start, grid)}
        answer.append(output)
    return json.dumps(answer)