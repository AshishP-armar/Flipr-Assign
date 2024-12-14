# Flipr Company Assignment

## E-Commerce API

This project is an API for an e-commerce website, providing functionalities for managing products, user authentication, cart operations, and orders.

## Features

- **User Authentication**
  - User Sign-up
  - User Sign-in (JWT-based authentication)

- **Product Management**
  - Add products
  - View product details
  - Update Product
  - Delete Product

- **Cart Management**
  - Add items to cart
  - View cart items
  - Remove items from cart
  - Update cart items

- **Order Management**
  - Place orders
  - View order history

## Technologies Used

- **Backend Framework**: Flask
- **Database**: MySQL 
- **Authentication**: JSON Web Tokens (JWT)
- **Development Tools**: Postman for API testing, Git for version control

## API Endpoints

### Authentication
- **POST** `api_url/signup` - Create a new user account.
- **POST** `api_url/signin` - Authenticate and obtain a JWT.

### Products
- **POST** `api_url/addproduct` - Add a new product.
- **PUT** ` api_url/updateproduct/<product_id>` - Update the product based on product id.
- **DELETE** `api_url/deleteproduct/<int:product_id>` - Delete the product based on its id.
- **GET** `api_url/products` - To get product.

### Cart
- **POST** `api_url/cart/add` - Add an item to the cart.
- **GET** `api_url/cart` - View items in the cart.
- **PUT** `api_url/cart/update` - Update quantity of a cart item.
- **DELETE** `api_url/cart/delete` - Remove an item from the cart.

### Orders
- **POST** `api_url/placeorder` - Place an order.
- **GET** `api_url/getalloders` - View order history.
- **GET** `api_url/orders/customer/<custmer_id>` - To get orders by customer.

### **Project Structure**
```bash
├── app.py    # Main file.        
├── migrations # Database migraton.
├── routes/   # routes for product, cart, auth, order.
│   ├── auth_routes.py     # for signup and signin.
│   ├── cart_routes.py	   # for carts routes.
    ├── order_routes.py    # for order route.
│   └── product_routes.py  # for product route.
├── models.py     # Database define for all cart, auth, order,	product.
├── requirements.txt  # Python dependencies
├── admin.py          # for making.
└── README.md         # Project instructions.` 
```

## Installation
1. Make Virtual ENV:
```bash
python3 -m vevn .venv
. .venv/bin/actiavte   # To activate virtual env
```
2. Clone the repository:
   ```bash
   git clone https://github.com/AshishP-armar/Flipr-Assign.git
   cd Flipr-Assign
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt  # For Flask
   ```
4. DataBase: 
```bash
flask db init
flask migrate "migration applied"
flask db upgrade
```

## Contact

For queries or collaboration, reach out to:
- **Email**: ashishparmar9817@gmail.com
- **LinkedIn**: [Ashish Parmar](https://www.linkedin.com/in/ashish-parmar-20b5a42bb)

---
