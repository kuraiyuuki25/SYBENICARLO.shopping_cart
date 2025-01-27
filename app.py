from flask import Flask, jsonify, request

app = Flask(__name__)

product_dimension = []
sales_orders = []

@app.route('/add-product', methods=['POST'])
def add_product():
    product_data = request.get_json()

    if not all(k in product_data for k in ("name", "price", "dimension")):
        return jsonify({"error": "Missing required fields: name, price, or dimension"}), 400
    
    product_id = len(product_dimension) + 1  
    product_data["id"] = product_id
    product_dimension.append(product_data)

    return jsonify({
        "message": f"Product {product_data['name']} added successfully.",
        "product": product_data
    })

@app.route('/view-items', methods=['GET'])
def view_items():
    if not product_dimension:
        return jsonify({"message": "No products available."}), 404
    return jsonify({"products": product_dimension})

@app.route('/purchase-order', methods=['POST'])
def purchase_order():
    order_data = request.get_json()
    product_id = order_data.get("product_id")
    quantity = order_data.get("quantity")
    
    product = next((item for item in product_dimension if item["id"] == product_id), None)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    total_price = product["price"] * quantity
    
    sales_order = {
        "order_id": len(sales_orders) + 1,
        "product_id": product_id,
        "quantity": quantity,
        "total_price": total_price
    }
    sales_orders.append(sales_order)
    
    return jsonify({
        "message": f"Order placed successfully for {quantity} {product['name']}(s)",
        "total_price": total_price,
        "order_id": sales_order["order_id"]
    })

if __name__ == '__main__':
    app.run(debug=True)
