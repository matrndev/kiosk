from __main__ import app, orders
from flask import render_template, request, redirect
import math

@app.route("/tip", methods=["GET"])
def tip_route():
    tip_amounts = []
    orderID = request.cookies.get('current_order')
    total = orders.find({"id": orderID})[0]["total"]
    t15 = math.trunc(total * 15/100)
    t20 = math.trunc(total * 20/100)
    t25 = math.trunc(total * 25/100)
    tip_amounts.append(t25)
    tip_amounts.append(t20)
    tip_amounts.append(t15)
    return render_template("tip/tip.html", tip_amounts=tip_amounts)

@app.route("/tip/add", methods=["GET"])
def tip_add_route():
    value = request.args.get("value")
    orderID = request.cookies.get('current_order')
    total = orders.find({"id": orderID})[0]["total"]
    newtotal = total + float(value)
    orders.update_one({"id": orderID}, {"$set": {"total": newtotal, "usedTip": value}})
    return redirect("/location")