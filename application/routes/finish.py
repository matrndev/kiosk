from __main__ import app, orders, coupons, delivery_options, rooms, modifications, p, socketio
from flask import render_template, request, make_response
from escpos.printer import Usb
from bson import json_util
from datetime import datetime

@app.route("/finish", methods=["GET"])
def finish_route():
    orderID = request.cookies.get("current_order")
    order = orders.find({"id": orderID})[0]
    print(order)
    try:
        coupon = coupons.find({"id": order["usedCoupon"]})[0]
    except:
        coupon = {"name": "none", "sale_percentage": 0}
    location = delivery_options.find({"id": order["delivery_option"]})[0]["friendly_name"]
    room = rooms.find({"id": order["room"]})[0]["friendly_name"]
    return render_template("finish/check.html", orderitems=order["items"], couponname=coupon["name"], couponsale=coupon["sale_percentage"], tipprice=order["usedTip"], location=location, room=room, total=order["total"])

@app.route("/finish/done", methods=["GET"])
def finish_done_route():
    now = datetime.now()
    order = orders.find({"id": request.cookies.get("current_order")})[0]
    orderID = request.cookies.get("current_order")
    orders.update_one({"id": orderID}, {"$set": {"status": "created", "datetime": now.strftime("%d/%m/%Y %H:%M:%S")}})
    location = delivery_options.find({"id": order["delivery_option"]})[0]["friendly_name"]
    room = rooms.find({"id": order["room"]})[0]["code"]
    
    response = make_response(render_template("finish/done.html", location=location, room=room, total=order["total"]))
    response.delete_cookie("current_order")
    

    p.set(align="center")
    #p.image("/home/pi/Pictures/logo.png")
    p.set(align='center', font='b', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.text("\nBig Coffee Ltd.\n")
    p.text("1403 Road St\n")
    p.text("New York, NY 10001\n")
    p.text("────────────────────────────────────────────────────────\n")
    p.set(align='left', font='a', bold=True, underline=0, width=2, height=2, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.textln("Room " + room)
    p.set(align='left', font='a', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.textln("Deliver to: " + location)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    p.textln("Ordered at: " + dt_string)
    p.textln("Order ID: " + order["id"])
    p.set(align='left', font='b', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.text("────────────────────────────────────────────────────────\n")
    p.set(align='left', font='a', bold=True, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.text("ITEM NAME                            PRICE\n")
    p.set(align='left', font='a', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    
    for item in order["items"]:
        p.textln("{:<20}{:>22}".format(item["item_name"], str(item["item_price"]) + " EUR"))
        if not item["recipient"] == "":
            p.textln(" Name: " + str(item["recipient"]))
        for mod in item["modifications"]:
            p.textln("{:<20}{:>22}".format(" + " + str(modifications.find({"id": mod})[0]["name"]), str(modifications.find({"id": mod})[0]["price"]) + " EUR"))
    p.set(align='left', font='b', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.text("────────────────────────────────────────────────────────\n")
    p.set(align='left', font='a', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.textln("Tip: " + order["usedTip"] + " EUR")
    try:
        p.textln("Sleva: " + str(coupons.find({"id": order["usedCoupon"]})[0]["sale_percentage"]) + " %") # TODO: this does NOT work
    except:
        pass
    
    p.set(align='left', font='a', bold=True, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=True, double_height=False, custom_size=False)
    p.textln("\nTotal: " + str(order["total"]) + " EUR")
    p.set(align='left', font='b', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.text("────────────────────────────────────────────────────────\n")
    p.set(align='left', font='a', bold=True, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    p.text("Customer's signature:\n")
    p.text("\n\n\n\n")
    p.text("__________________________________________\n\n")
    p.set(align='center', font='b', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=True, flip=False, double_width=False, double_height=False, custom_size=True)
    #p.qr(str("total") + ">" + str("room"),native=True,size=8)
    p.barcode("{B" + order["id"], "CODE128", pos="OFF")
    p.cut()
    socketio.emit('kitchen_update', {"id": order["id"], "room": room, "location": location, "items": order["items"], "time": now.strftime("%H:%M:%S")})
    return response


