import logging
import json

from flask import request, jsonify
from copy import deepcopy

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stonks', methods=['POST'])
def evaluatesoptopt():
    def solve(input):
        energy = input['energy']
        capital = input['capital']
        timeline = input['timeline']
        ans = 0
        path = list()
        if energy > 3:
            return path
        def recurse(current_timeline, energy_left, capital_left, current_year, portfolio, current_path):
            nonlocal ans, path
            if energy_left == 0:
                if current_year != "2037":
                    return
                # portfolio should contain (name, bought_price)
                for name, _ in portfolio:
                    if name in current_timeline[current_year].keys():
                        current_path.append("s-{}-1".format(name))
                        capital_left += current_timeline[current_year][name]['price']
                if capital_left > ans:
                    ans = capital_left
                    path = deepcopy(current_path)
            else:
                # buy or sell
                for stock in current_timeline[current_year].keys():
                    price, quantity = current_timeline[current_year][stock]['price'], current_timeline[current_year][stock]['qty']
                    if quantity > 0 and price <= capital_left:
                        # buy and recurse
                        next_timeline = deepcopy(current_timeline)
                        next_timeline[current_year][stock]['qty'] -= 1
                        next_portfolio = deepcopy(portfolio)
                        next_portfolio.append((stock, price))
                        next_path = deepcopy(current_path)
                        next_path.append("b-{}-1".format(stock))
                        recurse(next_timeline, energy_left, capital_left - price, current_year, next_portfolio, next_path)
                for i, (stock, bought_price) in enumerate(portfolio):
                    if stock in current_timeline[current_year].keys() and current_timeline[current_year][stock]['price'] > bought_price:
                        price = current_timeline[current_year][stock]['price']
                        next_timeline = deepcopy(current_timeline)
                        next_portfolio = [x for pos, x in enumerate(portfolio) if i != pos]
                        next_path = deepcopy(current_path)
                        next_path.append("s-{}-1".format(stock))
                        recurse(next_timeline, energy_left, capital_left + price, current_year, next_portfolio, next_path)
                for next_year in timeline.keys():
                    next_path = deepcopy(current_path)
                    if next_year != current_year:
                        next_path.append("j-{}-{}".format(current_year, next_year))
                    recurse(current_timeline, energy_left - 1, capital_left, next_year, portfolio, next_path)
        recurse(deepcopy(timeline), energy, capital, "2037", list(), list())
        return path

    input = eval(request.data)
    answer = list()
    for testcase in input:
        answer.append(solve(testcase))
    logging.info(answer)
    return json.dumps(answer)