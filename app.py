from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes.auth_routes import auth
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['JWT_SECRET_KEY'] = 'Atp@4466'

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(order_bp, url_prefix='/orders')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
