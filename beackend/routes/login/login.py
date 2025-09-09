from flask import Blueprint, jsonify, request
from jsonschema import validate as jsonschema_validate, ValidationError
from beackend.schemas import REQUEST_SCHEMAS_BY_ROUTE, RESPONSE_SCHEMAS_BY_ROUTE

from beackend.database.connection import Connection
from beackend.services.login_service import LoginService
from beackend.services.dto import (
    LoginRequestDTO,
    VerifyTokenDTO,
    RegisterUserDTO,
    CreateSystemUserDTO,
)


register = Blueprint("login", __name__)


def _service() -> LoginService:
    session = Connection().get_session()
    return LoginService(session)


@register.route('/get_token/<string:username>/<string:password>', methods=['GET'])
def login_user(username: str, password: str):
    dto = LoginRequestDTO(username=username, password=password)
    token = _service().authenticate_user(dto)
    if token is not None:
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@register.route('/verify_token', methods=['POST'])
def verify_token():
    data = request.get_json()
    dto = VerifyTokenDTO(token=data.get("token"))
    decoded = _service().verify_token(dto)
    if decoded is None:
        return jsonify({"valid": False}), 401
    return jsonify({"valid": True, "payload": decoded}), 200


@register.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    dto = RegisterUserDTO(
        id=data.get("id"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        phone_number=data.get("phone_number"),
        reputation_score=data.get("reputation_score", 0),
    )
    result = _service().register_user(dto)
    if "error" in result:
        return jsonify({"message": result["error"]}), result["status"]
    return jsonify({"message": "User registered successfully", "user_id": result["user_id"]}), 201


@register.route('/create_system_user/<int:user_id>', methods=['POST'])
def create_system_user(user_id: int):
    data = request.get_json()
    dto = CreateSystemUserDTO(
        user_id=user_id,
        system_user_name=data.get("system_user_name"),
        password=data.get("password"),
        role=data.get("role"),
    )
    validate = _service().is_system_user_exist(dto.system_user_name)
    if not validate:
        return jsonify({"message": "The System User exist. please try agen. "}), 404
    result = _service().create_system_user(dto)
    if "error" in result:
        return jsonify({"message": result["error"]}), result["status"]
    return jsonify({"message": "System user created successfully", "system_user_id": result["system_user_id"]}), 201
    
@register.route('/validate', methods=['POST', 'OPTIONS'])
def validate_payload():
    data = request.get_json(silent=True) or {}
    schema_type = (data.get('type') or 'request').lower()
    route = data.get('route')
    payload = data.get('payload')

    if not route or payload is None:
        return jsonify({"valid": False, "error": "Missing 'route' or 'payload'"}), 400

    schema_map = REQUEST_SCHEMAS_BY_ROUTE if schema_type == 'request' else RESPONSE_SCHEMAS_BY_ROUTE
    schema = schema_map.get(route)
    if not schema:
        return jsonify({"valid": False, "error": f"No schema found for route '{route}' and type '{schema_type}'"}), 404

    try:
        jsonschema_validate(instance=payload, schema=schema)
        return jsonify({"valid": True}), 200
    except ValidationError as ve:
        return jsonify({
            "valid": False,
            "error": ve.message,
            "path": list(ve.path),
            "schema_path": list(ve.schema_path)
        }), 400
