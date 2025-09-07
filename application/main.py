# import packages
from flask import Flask, render_template, request
import shortuuid
import socket
from pymongo import MongoClient
from flask_socketio import SocketIO
from escpos.printer import Usb
from bson import json_util

# init flask
app = Flask(__name__)
socketio = SocketIO(app) # , async_mode='gevent'

# init mongodb
client = MongoClient("YOUR_MONGODB_URI") #! REPLACE THIS!!!
db = client["kiosk"] #! change to your collection name

# init printer
p = Usb(0x04b8, 0x0202) # your printer may need a different address
#p = None

# assign db variables
orders = db["orders"]
rooms = db["rooms"]
customers = db["customers"]
userdata = db["userdata"]
sections = db["sections"]
items = db["items"]
modifications = db["modifications"]
coupons = db["coupons"]
delivery_options = db["delivery_options"]

# assign other variables
newuser = False
newadmintoken = ""

if userdata.find_one() == None:
    # new user
    newuser = True
    newadmintoken = shortuuid.ShortUUID().random(length=8)
    print("empty userdata")
    userdata.insert_one({"username": "admin", "password": newadmintoken, "uuid": shortuuid.uuid(), "permissions": ["administrator"]})
    print("Welcome! An admin account has been created for you.\nKiosk running at http://" + socket.getfqdn() + ":5961\nAdmin account: username 'admin' and password '" + newadmintoken + "'.")

@app.route('/')
def index():
    global newuser
    if newuser == False:
        return render_template("carousel.html")
    else:
        newuser = False
        return render_template("new.html", password=newadmintoken, address="http://" + socket.getfqdn() + ":4961")

# import other routes
import routes.items
import routes.coupon
import routes.order
import routes.tip
import routes.location
import routes.finish
import routes.recipient
import routes.kitchen


if __name__ == "__main__":
    #app.run(port=5961)
    #import waitress
    #waitress.serve(app=app, port=5961)
    socketio.run(app, host="0.0.0.0", port=5961)