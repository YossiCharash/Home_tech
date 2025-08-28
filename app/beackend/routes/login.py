from flask import Blueprint, jsonify, request
import jwt
import datetime
import requests
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from app.beackend.config import BaseConfig
from app.beackend.database.models.system_user import SystemUsers

# Secret key for signing JWT tokens
SECRET_KEY = "your_secret_key"

# Mock user data for demonstration
MOCK_USER = {
    "username": "testuser",
    "password": "password123"
}

register = Blueprint("login", __name__)


@register.route('/get_token', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    # Validate user credentials
    if username == MOCK_USER["username"] and password == MOCK_USER["password"]:
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm=BaseConfig().JWT_ALGORITHM
        )
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[BaseConfig().JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@register.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return jsonify({"message": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password)

    new_user = Users(
        system_username=username,
        password_hash=hashed_password,
        role=role
    )

    session = Session()
    try:
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"message": "Username already exists"}), 409
    except Exception as e:
        session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    finally:
        session.close()