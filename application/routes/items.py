from __main__ import app, sections, items, modifications, orders
from flask import render_template, request, make_response, redirect
import shortuuid

@app.route("/items", methods=["GET"])
def items_route():
    sectionID = 0
    order_total = 0
    orderID = request.cookies.get('current_order')
    if not request.args.get("section") == None:
        sectionID = int(request.args.get("section"))

    if orderID == None:
        response = make_response(render_template("items/select.html", sections=sections.find(), sectionID=sectionID, items=list(items.find()), order_total=0))
        response.set_cookie("current_order", shortuuid.ShortUUID().random(length=11))
    else:
        try:
            order_total = orders.find({"id": orderID})[0]["total"]
        except:
            pass
        if request.args.get("newItem") == "1":
            response = make_response(render_template("items/select.html", sections=sections.find(), sectionID=sectionID, items=list(items.find({"section": int(sectionID)})), order_total=order_total, newItem=True, showNext=True))
        else:
            if list(orders.find({"id": orderID})) == []:
                response = make_response(render_template("items/select.html", sections=sections.find(), sectionID=sectionID, items=list(items.find({"section": int(sectionID)})), order_total=order_total))
            else:
                response = make_response(render_template("items/select.html", sections=sections.find(), sectionID=sectionID, items=list(items.find({"section": int(sectionID)})), order_total=order_total, showNext=True))
    return response

@app.route("/items/add", methods=["GET"])
def add_route():
    itemID = request.args.get("id")
    item = items.find({"id": itemID})[0]
    orderID = request.cookies.get('current_order')
    order = list(orders.find({"id": orderID}))
    selectSectionID = request.args.get("selectSection")
    sectionID = 0
    
    # add to cart
    print(order)
    if order == []:
        orders.insert_one({"id": orderID, "total": item["price"], "items": [{"item_id": item["id"], "item_name": item["name"], "item_price": item["price"], "modifications": [], "recipient": ""}]})
    else:
        orders.update_one({"id": orderID}, {"$set": {"total": order[0]["total"] + item["price"]}, "$push": {"items": {"item_id": item["id"], "item_name": item["name"], "item_price": item["price"], "modifications": [], "recipient": ""}}})
    
    # handle modifications
    if list(items.find({"id": itemID, "modifications.modification_section": 0})) == []:
        return redirect("/items?newItem=1&section=" + selectSectionID)
    item_modifications = []
    for modification in item["modifications"]:
        if modification["modification_section"] < 1:
            item_modifications.append(modifications.find({"id": modification["modification_id"]})[0])
    
    return render_template("items/item.html", item_id=item["id"], item_name=item["name"], modifications=item_modifications, next_section=1, section=sectionID, required=item["required_sections"], total=items.find({"id": itemID})[0]["price"])

@app.route("/items/append_modification", methods=["GET"])
def append_modification_route():
    # TODO: ability to subtract modifications
    subtract = request.args.get("subtract")
    itemID = request.args.get("item_id")
    item = items.find({"id": itemID})[0]
    orderID = request.cookies.get('current_order')
    order = orders.find({"id": orderID})[0]
    modID = request.args.get("modification_id")
    sectionID = int(request.args.get("next_section"))
    # append modification
    if not modID == None:
        if subtract == "1":
            """order = orders.find({"id": orderID})[0]
            mod = modifications.find({"id": modID})[0]
            modCount = 0
            for onemod in order["modifications"]:
                if modID in onemod:
                    modCount = modCount + 1 
            orders.update_one({"id": orderID}, {"$set": {"total": order["total"] - mod["price"]*modCount}})
            orders.update_one({"id": orderID}, {"$pull": {"modifications": modID + ":" + itemID}}) # id of modification belongs to id of item
            """
            if modID in order["items"][-1]["modifications"]:
                edited_order = order
                edited_order["items"][-1]["modifications"].pop(-1)
                print(edited_order)
                orders.replace_one({"id": orderID}, edited_order)
                mod = modifications.find({"id": modID})[0]
                orders.update_one({"id": orderID}, {"$set": {"total": order["total"] - mod["price"]}})
            else:
                print("nope")
                pass
        else:
            order = orders.find({"id": orderID})[0]
            edited_order = order
            edited_order["items"][-1]["modifications"].append(modID)
            print(edited_order)
            orders.replace_one({"id": orderID}, edited_order)
            mod = modifications.find({"id": modID})[0]
            orders.update_one({"id": orderID}, {"$set": {"total": order["total"] + mod["price"]}})
        

    # check if there are more modifications
    if list(items.find({"id": itemID, "modifications.modification_section": int(sectionID)})) == []:
        return redirect("/chooseRecipient?order_id=" + orderID)
        #return redirect("/items?newItem=1")
    # more modifications
    item_modifications = []
    for modification in item["modifications"]:
        if modification["modification_section"] == int(sectionID):
            item_modifications.append(modifications.find({"id": modification["modification_id"]})[0])
    """previous_item_modifications = []
    for mod_fullid in orders.find({"id": orderID})[0]["modifications"]:
        mod_id = mod_fullid.split(":")[0]
        previous_item_modifications.append(modifications.find({"id": mod_id})[0]["name"])
    """
    previous_item_modifications = []
    for modid in order["items"][-1]["modifications"]:
        previous_item_modifications.append(modifications.find({"id": modid})[0]["name"])

    next_sectionID = int(sectionID)
    if sectionID in item["required_sections"]:
        next_sectionID = int(sectionID)+1
    return render_template("items/item.html", item_id=item["id"], item_name=item["name"], modifications=item_modifications, section=sectionID, next_section=next_sectionID, previous_modifications=previous_item_modifications, required=item["required_sections"])
