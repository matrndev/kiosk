from __main__ import app, orders
from flask import render_template, request, make_response, redirect

@app.route("/kitchen", methods=["GET"])
def kitchen_route():
    play = None
    if request.args.get("finishOrder"):
        orderID = request.args.get("finishOrder")
        orders.update_one({"id": orderID}, {"$set": {"status": "finished"}})
        play = False
        return redirect("/kitchen")
    order_list = orders.find({"status": "created"})
    #order_list = reversed(list(order_list))
    song = "chime"
    if not order_list == [] and play == None:
        play = True
    if request.args.get("sao"):
        song = "sao"
    return render_template("kitchen/kitchendisplay.html", orders=order_list, play=play, song=song)