from __main__ import app, delivery_options, rooms, orders
from flask import render_template, request, redirect

room = ""
delivery = ""

@app.route("/location", methods=["GET"])
def location_route():
    global room
    global delivery
    room = ""
    delivery = ""
    return render_template("location/location.html", delivery_options=delivery_options.find(), rooms=rooms.find())

@app.route("/location/choose", methods=["GET"])
def location_choose_route():
    global room
    global delivery
    canContinue = False
    if request.args.get("type") == "delivery":
        delivery = request.args.get("id")
    elif request.args.get("type") == "room":
        room = request.args.get("id")
    if not room == "" and not delivery == "":
        canContinue = True
    return render_template("location/location.html", delivery_options=delivery_options.find(), rooms=rooms.find(), room=room, delivery=delivery, canContinue=canContinue)

@app.route("/location/unchoose", methods=["GET"])
def location_unchoose_route():
    global room
    global delivery
    if request.args.get("type") == "delivery":
        delivery = ""
    elif request.args.get("type") == "room":
        room = ""
    return render_template("location/location.html", delivery_options=delivery_options.find(), rooms=rooms.find(), room=room, delivery=delivery)

@app.route("/location/continue", methods=["GET"])
def location_continue_route():
    global room
    global delivery
    if not room == "" and not delivery == "":
        orders.update_one({"id": request.cookies.get("current_order")}, {"$set": {"room": room, "delivery_option": delivery}})
        return redirect("/finish")
    else:
        return "not yet"