from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from BBDP import database
import json


app = Flask(__name__)

@app.route('/api/bar', methods=["GET"])
def get_bars():
    print("client is asking bar info...")
    return jsonify(database.get_bars())

@app.route('/api/bar/<name>', methods=["GET"])
def find_bar(name):
    try:
        if name is None:
            raise ValueError("Bar is not specified.")
            bar = database.find_bar(name)
        if bar is None:
            return make_response("No bar found with the given name.", 404)
        return jsonify(bar)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/beers_cheaper_than', methods=["POST"])
def find_beers_cheaper_than():
    body = json.loads(request.data)
    max_price = body['maxPrice']
    return jsonify(database.filter_beers(max_price))

@app.route('/api/menu/<name>', methods=['GET'])
def get_menu(name):
    try:
        if name is None:
            raise ValueError('Bar is not specified.')
        bar = database.find_bar(name)
        if bar is None:
            return make_response("No bar found with the given name.", 404)
        return jsonify(database.get_bar_menu(name))
    except ValueError as e:
            return make_response(str(e), 400)
    except Exception as e:
            return make_response(str(e), 500)

@app.route('/api/frequents-data', methods=['GET'])
def get_bar_frequent_counts():
    try:
        return jsonify(database.get_bar_frequent_counts())
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/drinker', methods=["GET"])
def get_drinkers():
    print("client is asking drinkers info...")
    return jsonify(database.get_drinkers())

@app.route('/api/drinker/bar/<drinker>', methods=["GET"])
def get_bar_names_by_drinker(drinker):
    try:
        if drinker is None:
            raise ValueError("Drinker is not specified.")
        print("client is asking bars info for drinker "+drinker+"...")
        bar_names = database.get_bar_names_by_drinker(drinker)
        return jsonify(bar_names)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/transaction', methods=["GET"])
def get_transactions():
    print("client is asking transactions info...")
    return jsonify(database.get_transactions())

@app.route('/api/transaction/<drinker>', methods=["GET"])
def get_transactions_by_drinker(drinker):
    try:
        if drinker is None:
            raise ValueError("Drinker is not specified.")
        print("client is asking transactions for drinker "+drinker+"...")
        transactions = database.get_transactions_by_drinker(drinker)
        return jsonify(transactions)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("transactions exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/transaction/<drinker>/<bar>', methods=["GET"])
def get_transactions_by_drinker_bar(drinker, bar):
    try:
        if drinker is None:
            raise ValueError("Drinker is not specified.")
        if bar is None:
            raise ValueError("Bar is not specified.")
        print("client is asking transactions for drinker "+drinker+" and bar "+bar+"...")
        transactions = database.get_transactions_by_drinker_bar(drinker, bar)
        return jsonify(transactions)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/drinker/beer_orders/<drinker>/<bar>', methods=["GET"])
def get_beer_orders_by_drinker(drinker, bar):
    try:
        if drinker is None:
            raise ValueError("Drinker is not specified.")
        print("client is asking beer orders for drinker "+drinker+"...")
        beer_orders = database.get_beer_orders_by_drinker(drinker, bar)
        return jsonify(beer_orders)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("beer_orders exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/drinker/bar_spendings/<drinker>/<bar>/<start_date>/<end_date>', methods=["GET"])
def get_bar_spendings_by_drinker(drinker, bar, start_date, end_date):
    try:
        if drinker is None:
            raise ValueError("Drinker is not specified.")
        if start_date is None:
            raise ValueError("start_date is not specified.")
        if end_date is None:
            raise ValueError("end_date is not specified.")
        print("client is asking beer orders for drinker "+drinker+" between "+start_date+" and "+end_date+"...")
        bar_spendings = database.get_bar_spendings_by_drinker(drinker, bar, start_date, end_date)
        return jsonify(bar_spendings)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("bar_spendings exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/bar/drinker_spendings/<bar>', methods=["GET"])
def get_drinker_spendings_by_bar(bar):
    try:
        if bar is None:
            raise ValueError("Bar is not specified.")
        print("client is asking drinker spendings by bar "+bar+"...")
        drinker_spendings = database.get_drinker_spendings_by_bar(bar)
        return jsonify(drinker_spendings)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/bar/beer_orders/<bar>', methods=["GET"])
def get_beer_orders_by_bar(bar):
    try:
        if bar is None:
            raise ValueError("Bar is not specified.")
        print("client is asking beer orders by bar "+bar+"...")
        beer_orders = database.get_beer_orders_by_bar(bar)
        return jsonify(beer_orders)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/bar/manf_beer_orders/<bar>', methods=["GET"])
def get_manf_beer_orders_by_bar(bar):
    try:
        if bar is None:
            raise ValueError("Bar is not specified.")
        print("client is asking manufacture beer orders by bar "+bar+"...")
        beer_orders = database.get_manf_beer_orders_by_bar(bar)
        return jsonify(beer_orders)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/bar/sales/<bar>/<start_date>/<end_date>', methods=["GET"])
def get_bar_sales(bar, start_date, end_date):
    try:
        if bar is None:
            raise ValueError("Bar is not specified.")
        if start_date is None:
            raise ValueError("start_date is not specified.")
        if end_date is None:
            raise ValueError("end_date is not specified.")
        print("client is asking sales for bar "+bar+" between "+start_date+" and "+end_date+"...")
        bar_sales = database.get_bar_sales(bar, start_date, end_date)
        return jsonify(bar_sales)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("bar_sales exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/beer', methods=["GET"])
def get_beers():
    print("client is asking beer info...")
    return jsonify(database.get_beers())

@app.route('/api/beer/bar_beer_orders/<beer>', methods=["GET"])
def get_beer_orders_for_bars(beer):
    try:
        if beer is None:
            raise ValueError("Beer is not specified.")
        print("client is asking beer orders for bars by beer "+beer+"...")
        bar_beer_orders = database.get_beer_orders_for_bars(beer)
        return jsonify(bar_beer_orders)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/beer/drinker_beer_orders/<beer>', methods=["GET"])
def get_beer_orders_for_drinkers(beer):
    try:
        if beer is None:
            raise ValueError("Beer is not specified.")
        print("client is asking beer orders for drinkers by beer "+beer+"...")
        drinker_beer_orders = database.get_beer_orders_for_drinkers(beer)
        return jsonify(drinker_beer_orders)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/beer/sales/<beer>/<start_date>/<end_date>', methods=["GET"])
def get_beer_sales(beer, start_date, end_date):
    try:
        if beer is None:
            raise ValueError("Beer is not specified.")
        if start_date is None:
            raise ValueError("start_date is not specified.")
        if end_date is None:
            raise ValueError("end_date is not specified.")
        print("client is asking sales for beer "+beer+" between "+start_date+" and "+end_date+"...")
        beer_sales = database.get_beer_sales(beer, start_date, end_date)
        return jsonify(beer_sales)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("beer_sales exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/sql/<sqlstr>', methods=["GET"])
def run_custom_sql(sqlstr):
    try:
        print("client is asking to run sql "+sqlstr+"...")
        result = database.run_custom_sql(sqlstr)
        return jsonify(result)
    except ValueError as e:
        return jsonify(str(e))
        #return make_response(str(e), 400)
    except Exception as e:
        print("beer_sales exception:"+str(e))
        return jsonify(str(e))
        #return make_response(str(e), 500)

@app.route('/api/table/<table>', methods=["GET"])
def read_table(table):
    try:
        print("client is asking to read table "+table+"...")
        result = database.read_table(table)
        return jsonify(result)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("read table exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/price/<bar>/<itemtype>/<itemname>/<quantities>', methods=["GET"])
def get_price(bar, itemtype, itemname, quantities):
    try:
        print("client is asking to get price of item "+itemname+"...")
        result = database.get_price(bar, itemtype, itemname, quantities)
        return jsonify(result)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("get price exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/bill/add/<bar>/<drinker>/<total>/<tips>/<datetime>', methods=["GET"])
def add_bill_rec(bar, drinker, total, tips, datetime):
    try:
        print("client is asking to insert a bill...")
        result = database.add_bill_rec(bar, drinker, total, tips, datetime)
        return jsonify(result)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("insert a bill exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/billdetail/add/<bar>/<drinker>/<datetime>/<itemtype>/<itemname>/<quantities>', methods=["GET"])
def add_billdetail_rec(bar, drinker, datetime, itemtype, itemname, quantities):
    try:
        print("client is asking to insert a bill detail...")
        result = database.add_billdetail_rec(bar, drinker, datetime, itemtype, itemname, quantities)
        return jsonify(result)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("insert a bill detail exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/frequent/add/<bar>/<drinker>', methods=["GET"])
def add_frequent(bar, drinker):
    try:
        print("client is asking to insert a frequent...")
        result = database.add_frequent(bar, drinker)
        return jsonify(result)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("insert a frequent exception:"+str(e))
        return make_response(str(e), 500)

@app.route('/api/sell/add/<bar>/<itemtype>/<itemname>/<price>', methods=["GET"])
def add_sell(bar, itemtype, itemname, price):
    try:
        print("client is asking to insert a sell...")
        result = database.add_sell(bar, itemtype, itemname, price)
        return jsonify(result)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        print("insert a sell exception:"+str(e))
        return make_response(str(e), 500)
