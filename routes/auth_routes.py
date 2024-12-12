from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
# @jwt_required()  # Optional JWT for admin creation
def signup():
    data = request.get_json()
    print("in signup")
    # Validate input data
    if not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({'error': 'Name, email, and password are required'}), 400

    name, email, password = data['name'], data['email'], data['password']
    print(name,email,password)
    address = data.get('address')
    is_admin = data.get('is_admin', False)  # Default to regular user
    print("hello")
    # Check if email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    print("hello")
    # Ensure only existing admins can create new admins
    if is_admin:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id) if current_user_id else None
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin access required to create admin users'}), 403
    print("user beifh")
    # Hash the password and create a new user
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password, address=address, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()
    print("dfofidghfoighro")
    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

@auth.route('/signin', methods=['POST'])
# @jwt_required()
def signin():
    data = request.get_json()
    email, password = data['email'], data['password']
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    session['is_admin'] = user.is_admin
    print(user.is_admin)
    session['user_id'] = user.id
    print(session.get("user_id"))
    token = create_access_token(identity=str(user.id))
    session["jwt"] = token
    return jsonify({'message': 'Login successful', 'token': token}), 200