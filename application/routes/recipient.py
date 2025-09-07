from __main__ import app, orders
from flask import render_template, request, make_response, redirect

@app.route("/chooseRecipient", methods=["GET"])
def choose_recipient_route():
    # this would be used to add a customer's name to the item to later identify who ordered what (stick a name onto the cup)
    #! not fully implemented yet!
    orderID = request.args.get("order_id")
    if request.args.get("recipient") == None:
        return redirect("/items?newItem=1") #! skip this feature for now
        #return render_template("recipient/chooserecipient.html", order_id=request.args.get("order_id"))
    order = orders.find({"id": orderID})[0]
    edited_order = order
    edited_order["items"][-1]["recipient"] = request.args.get("recipient")
    print(edited_order)
    orders.replace_one({"id": orderID}, edited_order)
    return redirect("/items?newItem=1")