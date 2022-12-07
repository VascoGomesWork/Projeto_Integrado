from flask import Flask, jsonify, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from models import db, Users, Tools, ToolsSchema
from config import ApplicationConfig
from flask_cors import CORS, cross_origin

# .\venv\Scripts\activate -> activate virtual envirement
# pip install -r .\requirements.txt

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

server_session = Session(app)
db.init_app(app)
with app.app_context():
    db.create_all()

# Get current user
@app.route("/@me")
def get_curretn_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = Users.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    })

# Get All Tools
@app.route("/stock", methods=["GET", "POST"])
def view_stock():
    stock = Tools.query.all()
    tools_schema = ToolsSchema(many=True)
    result = tools_schema.dump(stock)

    return jsonify({ "stock" : result })

# Add new tool
@app.route("/addtool", methods=["POST"])
def add_tool():
    name = request.json["name"]
    quantity = request.json["quantity"]

    new_tool = Tools(name=name, quantity=quantity)
    db.session.add(new_tool)
    db.session.commit()

    return jsonify({
        "id": new_tool.id,
        "name": new_tool.name,
        "quantity": new_tool.quantity
    })

# Remove tool
@app.route("/removetool", methods=["POST"])
def remove_tool():
    name = request.json["name"]
    quantity = request.json["quantity"]

    remove_tool = Tools.query.filter_by(name=name).first()
    remove_tool.quantity = int(quantity)
    db.session.commit()

    return jsonify({
        "id": remove_tool.id,
        "name": remove_tool.name,
        "quantity": remove_tool.quantity
    })

# Register route
@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    # Verifies if user exists
    user_exist = Users.query.filter_by(email=email).first() is not None
    if user_exist:
        return jsonify({"error": "User already exist"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = Users(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # SAVE SESSION
    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })

# Login route
@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    # Verifies if user exists
    user = Users.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    # SAVE SESSION
    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })

# Logout
@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


# Main
if __name__ == "__main__":
    app.run(debug=True)
