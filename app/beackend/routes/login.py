from flask import Blueprint, jsonify, request
import jwt
import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app.beackend.config import BaseConfig
from app.beackend.database.connection import Connection
from app.beackend.database.models.users import Users
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
    id = data.get("id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    reputation_score = data.get("reputation_score", 0)
    # username = data.get("username")
    # password = data.get("password")
    # role = data.get("role")

    if not id or not last_name or not first_name or not email or not phone_number:
        return jsonify({"message": "Missing required fields"}), 400

    # hashed_password = generate_password_hash(password)

    new_user = Users(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        reputation_score=reputation_score
    )
    # system_user = SystemUsers(
    #     system_username=username,
    #     password_hash=hashed_password,
    #     role=role,
    #     real_user=new_user
    # )
    try:
        connection = BaseConfig().get_connection()
        if not connection:
            raise ValueError("Failed to retrieve a valid database connection.")
        conn_instance = Connection(connection)  # Create an instance of Connection
        session = conn_instance.get_session()
        print(session)
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