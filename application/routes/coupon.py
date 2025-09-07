from __main__ import app, coupons, orders
from flask import render_template, request
import serial


@app.route("/coupon", methods=["GET"])
def coupon_route():
    try:
        # Open the serial port
        ser = serial.Serial('/dev/serial0', 9600, timeout=1)

        # Scanning command to send
        scanning_command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x02, 0x01, 0xAB, 0xCD])

        # Send the scanning command
        ser.write(scanning_command)
        print("Scanning command sent")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    finally:
        # Close the serial port
        ser.close()

    return render_template("coupon/coupon.html")

@app.route("/coupon/wake", methods=["GET"])
def wake_coupon_route():
    try:
        # Open the serial port
        ser = serial.Serial('/dev/serial0', 9600, timeout=1)

        # Scanning command to send
        scanning_command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x02, 0x01, 0xAB, 0xCD])

        # Send the scanning command
        ser.write(scanning_command)
        print("Scanning command sent")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return "error"
    finally:
        # Close the serial port
        ser.close()
        return 'ok'

@app.route("/coupon/apply_coupon", methods=["POST"])
def apply_coupon_route():
    orderID = request.cookies.get("current_order")
    couponID = request.form.get("coupon")
    order = list(orders.find({"id": orderID}))
    coupon = list(coupons.find({"id": couponID}))
    if coupon == []:
        return render_template("coupon/coupon.html", modal=True, error=True)
    orig_total = order[0]["total"]
    sale = coupon[0]["sale_percentage"]
    sale_total = orig_total - (orig_total * sale / 100)
    uses_left = coupon[0]["uses_left"]
    if uses_left == 0:
        return render_template("coupon/coupon.html", modal=True, error=True)
    else:
        orders.update_one({"id": orderID}, {"$set": {"total": sale_total, "usedCoupon": couponID}})
        coupons.update_one({"id": couponID}, {"$set": {"uses_left": uses_left - 1}})
        if uses_left == 0:
            coupons.delete_one({"id": couponID})
        return render_template("coupon/coupon.html", modal=True, applied=True, salepercentage=sale, remaining=uses_left-1, total=sale_total)
