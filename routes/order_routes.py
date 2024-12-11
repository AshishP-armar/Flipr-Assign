from flask import Blueprint, request, jsonify
from models import Order, Cart, Product, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/placeorder', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    shipping_address = data.get('shipping_address')

    if not shipping_address:
        return jsonify({'error': 'Shipping address is required'}), 400

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'error': 'Your cart is empty'}), 400

    # Calculate total order cost and validate stock
    total_cost = 0
    order_details = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if not product:
            return jsonify({'error': f'Product with ID {item.product_id} not found'}), 404

        total_cost += product.price * item.quantity
        order_details.append({
            'product_id': product.id,
            'name': product.name,
            'quantity': item.quantity,
            'price': product.price,
            'total': product.price * item.quantity
        })

    # Create Order
    order = Order(
        user_id=user_id,
        shipping_address=shipping_address,
        order_date=datetime.utcnow()
    )
    db.session.add(order)
    db.session.commit()

    # Clear the cart after placing the order
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    return jsonify({
        'message': 'Order placed successfully',
        'order_id': order.id,
        'total_cost': total_cost,
        'order_details': order_details
    }), 201


@order_bp.route('/getallorders', methods=['GET'])
@jwt_required()
def get_all_orders():
    orders = Order.query.all()
    if not orders:
        return jsonify({'message': 'No orders found'}), 404

    order_list = []
    for order in orders:
        order_list.append({
            'order_id': order.id,
            'user_id': order.user_id,
            'shipping_address': order.shipping_address,
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({'orders': order_list}), 200


@order_bp.route('/orders/customer/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_orders_by_customer(customer_id):
    orders = Order.query.filter_by(user_id=customer_id).all()
    if not orders:
        return jsonify({'message': f'No orders found for customer ID {customer_id}'}), 404

    order_list = []
    for order in orders:
        order_list.append({
            'order_id': order.id,
            'shipping_address': order.shipping_address,
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({'orders': order_list}), 200
