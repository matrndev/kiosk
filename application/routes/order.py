from __main__ import app, orders
from flask import render_template, request, make_response, redirect

@app.route("/order/cancel", methods=["GET"])
def cancel_route():
    orderID = request.cookies.get("current_order")
    orders.delete_one({"id": orderID})
    response = make_response(redirect("/"))
    response.delete_cookie("current_order")
    return response

@app.route("/order/edit/items", methods=["GET"])
def edit_items_route():
    orderID = request.cookies.get("current_order")
    return render_template("order/edititems.html")