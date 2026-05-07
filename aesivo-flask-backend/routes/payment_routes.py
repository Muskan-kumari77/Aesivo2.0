from flask import Blueprint, request, jsonify, current_app
import razorpay

payment_bp = Blueprint("payment", __name__)

client = razorpay.Client(auth=("rzp_test_SmZH8R2cfV0Mz8", "AS1zo9ecQvt4A4w5XE0rHKSP"))


@payment_bp.route("/create-order", methods=["POST"])
def create_order():
    data = request.json

    amount = int(data["amount"] * 100)  # paisa

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify(order)
@payment_bp.route("/verify", methods=["POST"])
def verify_payment():
    data = request.json

    client.utility.verify_payment_signature({
        'razorpay_order_id': data['order_id'],
        'razorpay_payment_id': data['payment_id'],
        'razorpay_signature': data['signature']
    })

    return jsonify({"status": "verified"})