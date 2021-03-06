from sqlalchemy import create_engine
from sqlalchemy import sql
import time
from datetime import datetime
#from sqlalchemy import database_exists, create_database

from BBDP import config

engine = create_engine(config.database_uri,isolation_level="AUTOCOMMIT")
#engine = create_engine(config.database_uri)
#print(database_exists(engine.url))
print(engine)
print("Engine starts!")


def get_bars():
    #Connect to the database and retrieve a list of all the bars and their informatio
    with engine.connect() as con:
        rs = con.execute("SELECT name, license, city, phone, addr FROM bars;")
        #print("Asking bar info:  " +rs)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Bars result: "+str(results))
        return results

def find_bar(name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT name, license, city, phone, addr FROM bars WHERE name = :name;"
            )
        rs = con.execute(query, name=name)
        result = rs.first()
        if result is None:
            return None
        return dict(result)

def filter_beers(max_price):
    with engine.connect() as con:
        query = sql.text(
            "SELECT * FROM sells WHERE price < :max_price;")
        rs = con.execute(query, max_price=max_price)
        results = [dict(row) for row in rs]
        for r in results:
            r['price'] = float(r['price'])
            return results


def get_bar_menu(bar_name):
    with engine.connect() as con:

        #query = sql.text(
        #    'SELECT a.bar, a.beer, a.price, b.manf as likes FROM sells as a JOIN beers AS b ON a.beer = b.name WHERE a.bar = :bar;')
        query = sql.text(
            'SELECT a.bar, a.beer, a.price, b.manf, coalesce(c.like_count, 0) as likes \
                FROM sells as a \
                JOIN beers AS b \
                ON a.beer = b.name \
                LEFT OUTER JOIN (SELECT beer, count(*) as like_count FROM likes GROUP BY beer) as c \
                ON a.beer = c.beer \
                WHERE a.bar = :bar; \
            ')

        rs = con.execute(query, bar=bar_name)
        results = [dict(row) for row in rs]
        for i, _ in enumerate(results):
            results[i]['price'] = float(results[i]['price'])
        return results

def get_bar_frequent_counts():
    with engine.connect() as con:
        query = sql.text('SELECT bar, count(*) as frequentCount FROM frequents GROUP BY bar;')
        rs = con.execute(query)
        results = [dict(row) for row in rs]
        return results

def get_drinkers():
    #Connect to the database and retrieve a list of all the bars and their informatio
    with engine.connect() as con:
        rs = con.execute("SELECT distinct name FROM drinkers;")
        results = []
        for row in rs:
            results.append(dict(row))
        #print("Drinkers result: "+str(results))
        return results

def get_bar_names_by_drinker(drinker):
    with engine.connect() as con:
        query = sql.text(
            "SELECT distinct bar FROM bills WHERE drinker = :drinker;"
            )
        rs = con.execute(query, drinker=drinker)
        results = []
        for row in rs:
            results.append(dict(row))
        #print("Bars-by-drinker result: "+str(results))
        return results

def get_transactions():
    with engine.connect() as con:
        query = sql.text(
            "SELECT drinker, bar, CAST(total AS char) AS total, CAST(tips AS char) AS tips, datetime FROM bills ORDER BY datetime DESC, bar, drinker"
            )
        rs = con.execute(query)
        results = []
        for row in rs:
            results.append(dict(row))
        #print("Transactions result: "+str(results))
        return results

def get_transactions_by_drinker(drinker):
    with engine.connect() as con:
        query = sql.text(
            "SELECT drinker, bar, CAST(total AS char) AS total, CAST(tips AS char) AS tips, datetime "\
            "FROM bills WHERE drinker = :drinker ORDER BY datetime DESC, bar;"
            )
        rs = con.execute(query, drinker=drinker)
        results = []
        for row in rs:
            results.append(dict(row))
        #print("Transactions_by_drinker result: "+str(results))
        return results

def get_transactions_by_drinker_bar(drinker, bar):
    with engine.connect() as con:
        query = sql.text(
            "SELECT drinker, bar, CAST(total AS char) AS total, CAST(tips AS char) AS tips, datetime "\
            "FROM bills WHERE drinker = :drinker AND bar = :bar ORDER BY datetime DESC;"
            )
        rs = con.execute(query, drinker=drinker, bar=bar)
        results = []
        for row in rs:
            results.append(dict(row))
        #print("Transactions_by_drinker_bar result: "+str(results))
        return results

def get_beer_orders_by_drinker(drinker, bar):
    with engine.connect() as con:
        sqlstr = "SELECT itemname, CAST(sum(D.quantities) AS char) AS quantities FROM bills B, billdetails D " \
            "WHERE B.bill_id = D.bill_id AND B.drinker = :drinker AND D.itemtype = 'beer' "
        if bar != "0":
            sqlstr = sqlstr + "AND B.bar = :bar "
        sqlstr = sqlstr + "GROUP BY D.itemname"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        if bar == "0":
            rs = con.execute(query, drinker=drinker)
        else:
            rs = con.execute(query, drinker=drinker, bar=bar)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Beer_orders_by_drinker result: "+str(results))
        return results

def get_bar_spendings_by_drinker(drinker, bar, start_date, end_date):
    with engine.connect() as con:
        sqlstr = "SELECT bar, CAST(sum(total) AS char) AS total FROM bills WHERE drinker = :drinker "
        if bar != "0":
            sqlstr = sqlstr + "AND bar = :bar "
        sqlstr = sqlstr + "AND datetime >= :start_date AND datetime <= :end_date GROUP BY bar"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        if bar == "0":
            rs = con.execute(query, drinker=drinker, start_date=start_date, end_date=end_date)
        else:
            rs = con.execute(query, drinker=drinker, bar=bar, start_date=start_date, end_date=end_date)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Beer_bar_spendings_by_drinker result: "+str(results))
        return results

def get_drinker_spendings_by_bar(bar):
    with engine.connect() as con:
        sqlstr = "SELECT drinker, CAST(sum(total) AS char) AS total FROM bills WHERE bar = :bar GROUP BY drinker"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Drinker_spendings_by_bar result: "+str(results))
        return results

def get_beer_orders_by_bar(bar):
    with engine.connect() as con:
        sqlstr = "SELECT itemname, CAST(sum(D.quantities) AS char) AS quantities FROM bills B, billdetails D " \
            "WHERE B.bill_id = D.bill_id AND B.bar = :bar AND D.itemtype = 'beer' GROUP BY D.itemname"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Beer_orders_by_bar result: "+str(results))
        return results

def get_manf_beer_orders_by_bar(bar):
    with engine.connect() as con:
        sqlstr = "SELECT E.manf, CAST(sum(D.quantities) AS char) AS quantities FROM bills B, billdetails D, "\
            "beers E WHERE B.bill_id = D.bill_id AND B.bar = :bar AND D.itemtype = 'beer' AND "\
            "D.itemname = E.name GROUP BY E.manf"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Manf_beer_orders_by_bar result: "+str(results))
        return results

def get_bar_sales(bar, start_date, end_date):
    with engine.connect() as con:
        sqlstr = "SELECT CAST(sum(total) AS char) AS total, datetime FROM bills WHERE bar = :bar "\
            "AND datetime >= :start_date AND datetime <= :end_date GROUP BY datetime ORDER BY datetime asc"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar, start_date=start_date, end_date=end_date)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Beer_bar_sales result: "+str(results))
        return results


def get_beers():
    #Connect to the database and retrieve a list of all the bars and their informatio
    with engine.connect() as con:
        rs = con.execute("SELECT distinct name FROM beers")
        #print("Asking bar info:  " +rs)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Beers result: "+str(results))
        return results


def get_beer_orders_for_bars(beer):
    with engine.connect() as con:
        sqlstr = "SELECT B.bar, CAST(sum(D.quantities) AS char) AS quantities FROM bills B, billdetails D " \
            "WHERE B.bill_id = D.bill_id AND D.itemtype = 'beer' AND D.itemname = :beer GROUP BY B.bar"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        rs = con.execute(query, beer=beer)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Beer_orders_for_bars result: "+str(results))
        return results

def get_beer_orders_for_drinkers(beer):
    with engine.connect() as con:
        sqlstr = "SELECT B.drinker, CAST(sum(D.quantities) AS char) AS quantities FROM bills B, billdetails D " \
            "WHERE B.bill_id = D.bill_id AND D.itemtype = 'beer' AND D.itemname = :beer GROUP BY B.drinker"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        rs = con.execute(query, beer=beer)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Beer_orders_for_drinkers result: "+str(results))
        return results

def get_beer_sales(beer, start_date, end_date):
    with engine.connect() as con:
        sqlstr = "SELECT CAST(sum(D.quantities) AS char) AS quantities FROM bills B, billdetails D "\
            "WHERE B.bill_id = D.bill_id AND D.itemtype = 'beer' AND D.itemname = :beer "\
            "AND B.datetime >= :start_date AND B.datetime <= :end_date GROUP BY B.datetime "\
            "ORDER BY B.datetime"
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        rs = con.execute(query, beer=beer, start_date=start_date, end_date=end_date)
        results = []
        for row in rs:
            results.append(dict(row))
        print("Beer_beer_sales result: "+str(results))
        return results

def run_custom_sql(sqlstr):
    with engine.connect() as con:
        print("sqlstr: " + sqlstr)
        query = sql.text(sqlstr)
        rs = con.execute(query)
        #results = []
        #for row in rs:
        #    results.append(dict(row))
        #print("custom SQL result: "+str(results))
        #return str(results)
        return "Complete"

def read_table(table):
    with engine.connect() as con:
        print("table: " + table)
        if table == "bills":
            sqlstr = "SELECT bill_id, drinker, bar, CAST(total AS char) AS total, "\
                "CAST(tips AS char) AS tips, datetime FROM bills LIMIT 20"
        elif table == "billdetails":
            sqlstr = "SELECT bill_id, itemname, itemtype, "\
                "CAST(quantities AS char) AS quantities FROM billdetails LIMIT 20"
        elif table == "bars":
            sqlstr = "SELECT name, license, addr, city, state, phone, "\
                "CAST(open AS char) AS open, CAST(close AS char) AS close FROM bars LIMIT 20"
        elif table == "beers" or table == "food" or table == "softdrinks":
            sqlstr = "SELECT name, manf FROM " + str(table)
        elif table == "drinkers":
            sqlstr = "SELECT name, addr, city, state, phone FROM drinkers"
        elif table == "frequents":
            sqlstr = "SELECT drinker, bar FROM frequents"
        elif table == "likes":
            sqlstr = "SELECT drinker, beer FROM likes"
        elif table == "sells":
            sqlstr = "SELECT bar, itemname, itemtype, CAST(price AS char) AS price FROM sells"
        query = sql.text(sqlstr)
        rs = con.execute(query)
        results = []
        for row in rs:
            results.append(dict(row))
        print("read table result: "+str(results))
        return results

def get_price(bar, itemtype, itemname, quantities):
    with engine.connect() as con:
        sqlstr = "SELECT CAST(price * :quantities AS char) AS price FROM sells "\
            "WHERE bar = :bar AND itemtype = :itemtype AND itemname = :itemname"
        query = sql.text(sqlstr)
        rs = con.execute(query, quantities=quantities,
            itemtype=itemtype, itemname=itemname, bar=bar)
        result = "0.0"
        for row in rs:
            result = str(row[0])
        print("read table result: "+str(result))
        return result

def add_bill_rec(bar, drinker, total, tips, datetimestr):
    #datetimestr='2018-11-18 19:30'
    print("converting datetime: "+datetimestr)
    datetime_object = datetime.strptime(datetimestr, '%Y-%m-%dT%H:%M')
    # '2018-11-18T19:30'
    print("datetime:"+str(datetime_object))
    time_object = datetime_object.time()
    print("time:"+str(time_object))
    #return ""

    with engine.connect() as con:
        sqlstr = "SELECT count(*) AS count FROM bars WHERE name = :bar AND open < :time_bill AND close > :time_bill"
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar, time_bill=time_object)
        for row in rs:
            count = row[0]
            print ("count:"+str(row[0]))
            break
        if count == 0:
            result = "Not accepted due to violation of assertion 1 - the bar is closed."
            return result

        sqlstr = "INSERT INTO bills (bar, drinker, total, tips, datetime) "\
            "VALUES (:bar, :drinker, :total, :tips, :datetime_field)"
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar, drinker=drinker, total=total,
            tips=tips, datetime_field=datetimestr)
        return ""

def add_billdetail_rec(bar, drinker, datetimestr, itemtype, itemname, quantities):
    with engine.connect() as con:
        bill_id = "0"
        num = 3
        while bill_id == "0" and num > 0:
            time.sleep(1)
            sqlstr = "SELECT bill_id FROM bills WHERE bar = :bar AND drinker = :drinker "\
                "AND datetime = :datetime_field"
            query = sql.text(sqlstr)
            rs = con.execute(query, bar=bar, drinker=drinker, datetime_field=datetimestr)
            for row in rs:
                bill_id = str(row[0])
            num = num - 1
            print("bill_id: "+str(bill_id))

        if bill_id == "0":
            result = "No valid bill id"
            return result

        sqlstr = "INSERT INTO billdetails (bill_id, itemname, itemtype, quantities) "\
            "VALUES (:bill_id, :itemname, :itemtype, :quantities)"
        query = sql.text(sqlstr)
        rs = con.execute(query, bill_id=bill_id, itemname=itemname, itemtype=itemtype,
            quantities=quantities)
        return ""

def add_frequent(bar, drinker):
    with engine.connect() as con:
        sqlstr = "SELECT count(*) AS count FROM bars B, drinkers D WHERE B.name = :bar "\
            "AND D.name = :drinker AND B.state = D.state"
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar, drinker=drinker)
        for row in rs:
            count = row[0]
            print ("count:"+str(row[0]))
            break
        if count == 0:
            result = "Not accepted due to violation of assertion 2 - the bar and the drinker are not in the same state."
            return result

        sqlstr = "INSERT INTO frequents (bar, drinker) VALUES (:bar, :drinker)"
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar, drinker=drinker)
        return ""

def add_sell(bar, itemtype, itemname, price):
    result = check_price_order(bar, itemtype, itemname, price, "less")
    if result != "" :
        return result
    result = check_price_order(bar, itemtype, itemname, price, "greater")
    if result != "" :
        return result

    with engine.connect() as con:
        sqlstr = "INSERT INTO sells (bar, itemtype, itemname, price) VALUES (:bar, :itemtype, :itemname, :price)"
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar, itemtype=itemtype, itemname=itemname, price=price)
        return ""

def check_price_order(bar, itemtype, itemname, price, which_half):
    with engine.connect() as con:
        sqlstr = "SELECT itemname FROM sells WHERE bar = :bar "\
            "AND itemtype = :itemtype AND itemname <> :itemname AND price "
        if which_half == "less":
            sqlstr = sqlstr + "<"
        else:
            sqlstr = sqlstr + ">"
        sqlstr = sqlstr + " :price"
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar, itemtype=itemtype, itemname=itemname, price=price)
        items = []
        for row in rs:
            items.append(row[0])
        print ("items: "+str(items))
        if len(items) == 0:
            return ""

        sqlstr = "SELECT bar, price FROM sells WHERE bar <> :bar "\
            "AND itemtype = :itemtype AND itemname = :itemname"
        query = sql.text(sqlstr)
        rs = con.execute(query, bar=bar, itemtype=itemtype, itemname=itemname)
        other_bars = []
        for row in rs:
            o_bar = {
                'bar': row[0],
                'price': row[1]
            };
            other_bars.append(o_bar)
        print ("other_bars: "+str(other_bars))

        for o_bar in other_bars:
            sqlstr = "SELECT count(*) AS count FROM sells WHERE bar <> :bar "\
                "AND itemtype = :itemtype AND price "
            if which_half == "less":
                sqlstr = sqlstr + ">"
            else:
                sqlstr = sqlstr + "<"
            sqlstr = sqlstr + " :price AND itemname IN ("
            num = 0
            for item in items:
                if num > 0:
                    sqlstr = sqlstr + ", "
                sqlstr = sqlstr + "\"" + item + "\""
                num = num + 1
            sqlstr = sqlstr + ")"

            query = sql.text(sqlstr)
            rs = con.execute(query, bar=o_bar['bar'], itemtype=itemtype, price=o_bar['price'])
            count = 0
            for row in rs:
                count = row[0]
                print ("count: "+str(count))
                break

            if count > 0:
                result = "Not accepted due to violation of assertion 3 - selling item is not in correct price order."
                return result

        return ""
