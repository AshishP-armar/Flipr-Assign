from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes.auth_routes import auth
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['JWT_SECRET_KEY'] = 'Atp@4466'
app.config['SECRET_KEY'] = 'Atp@4466'
app.config['SESSION_TYPE'] = 'filesystem' 
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

CORS(app, origins=["https://flipr-ef66.onrender.com"], methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], allow_headers=["Content-Type", "Authorization"])


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(order_bp, url_prefix='/orders')


def create_app():
    app = Flask(__name__)

    # Configuration settings for the app (example)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # Update as needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'Atp@4466'  # Update this with a secure secret key

    # Initialize the database and migration objects with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints (optional, if using Blueprints)
    from routes.auth_routes import auth  # Example, update with your actual routes file
    app.register_blueprint(auth, url_prefix='/auth')

    return app


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
