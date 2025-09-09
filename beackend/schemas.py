# JSON Schemas for request bodies of existing routes
# Can be used for validation or API tooling (e.g., Postman/Swagger converters)

GetTokenRequestSchema = {
    "type": "object",
    "required": ["username", "password"],
    "additionalProperties": False,
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1}
    }
}

VerifyTokenRequestSchema = {
    "type": "object",
    "required": ["token"],
    "additionalProperties": False,
    "properties": {
        "token": {"type": "string", "minLength": 1}
    }
}

RegisterUserRequestSchema = {
    "type": "object",
    "required": ["id", "first_name", "last_name", "email", "phone_number"],
    "additionalProperties": False,
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "first_name": {"type": "string", "minLength": 1},
        "last_name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "phone_number": {"type": "string", "minLength": 3},
        "reputation_score": {"type": "integer", "minimum": 0}
    }
}

CreateSystemUserRequestSchema = {
    "type": "object",
    "required": ["system_user_name", "password", "role"],
    "additionalProperties": False,
    "properties": {
        "system_user_name": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 6},
        "role": {"type": "string", "enum": ["admin", "moderator"]}
    }
}

# Optional: response schemas (basic shapes)
GetTokenResponseSchema = {
    "type": "object",
    "required": ["token"],
    "properties": {
        "token": {"type": "string"}
    }
}

VerifyTokenResponseSchema = {
    "type": "object",
    "required": ["valid"],
    "properties": {
        "valid": {"type": "boolean"},
        "payload": {"type": "object"}
    }
}

RegisterUserResponseSchema = {
    "type": "object",
    "required": ["message", "user_id"],
    "properties": {
        "message": {"type": "string"},
        "user_id": {"type": "integer", "minimum": 1}
    }
}

CreateSystemUserResponseSchema = {
    "type": "object",
    "required": ["message", "system_user_id"],
    "properties": {
        "message": {"type": "string"},
        "system_user_id": {"type": "integer", "minimum": 1}
    }
}

# Export mapping by route for convenience
REQUEST_SCHEMAS_BY_ROUTE = {
    "/get_token": GetTokenRequestSchema,
    "/verify_token": VerifyTokenRequestSchema,
    "/register": RegisterUserRequestSchema,
    "/create_system_user": CreateSystemUserRequestSchema,  # path param user_id is int
}

RESPONSE_SCHEMAS_BY_ROUTE = {
    "/get_token": GetTokenResponseSchema,
    "/verify_token": VerifyTokenResponseSchema,
    "/register": RegisterUserResponseSchema,
    "/create_system_user": CreateSystemUserResponseSchema,
}
