from flask import Flask, request, jsonify
import requests
from repository.order_repository import create_order, get_orders

app = Flask(__name__)

# User service running on different port
USER_SERVICE_URL = "http://localhost:5001"


def validate_user(user_id):
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False


@app.route("/orders", methods=["POST"])
def add_order():
    data = request.json

    user_id = data.get("user_id")
    product = data.get("product")
    quantity = data.get("quantity")

    if user_id is None or product is None or quantity is None:
        return jsonify({"error": "user_id, product and quantity are required"}), 400

    try:
        user_id = int(user_id)
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "user_id and quantity must be numbers"}), 400

    if quantity <= 0:
        return jsonify({"error": "quantity must be greater than 0"}), 400

    # Validate user from user service
    if not validate_user(user_id):
        return jsonify({"error": "User not found"}), 400

    order_id = create_order(user_id, product, quantity)

    return jsonify({
        "message": "Order created successfully",
        "order_id": order_id
    }), 201


@app.route("/orders", methods=["GET"])
def view_orders():
    orders = get_orders()
    return jsonify(orders), 200


if __name__ == "__main__":
    app.run(port=5002, debug=True)