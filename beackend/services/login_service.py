from typing import Optional, Dict, Any
from werkzeug.security import check_password_hash

import datetime
import jwt
from sqlalchemy.orm import Session

from beackend.config import BaseConfig
from beackend.clients.user_client import UserClient
from beackend.services.dto import (
    LoginRequestDTO,
    VerifyTokenDTO,
    RegisterUserDTO,
    CreateSystemUserDTO,
)


class LoginService:
    # Secret key for signing JWT tokens
    SECRET_KEY = "your_secret_key"

    def __init__(self, session: Session):
        self.session = session
        self.user_client = UserClient(session)

    def authenticate_user(self, dto: LoginRequestDTO) -> Optional[str]:
        """Authenticate and return JWT if valid."""
        hashed_password = self.user_client.get_password_hash(dto.username)
        if hashed_password and check_password_hash(hashed_password, dto.password):
            token = jwt.encode(
                {
                    "username": dto.username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                self.SECRET_KEY,
                algorithm=BaseConfig().JWT_ALGORITHM
            )
            return token
        return None

    def verify_token(self, dto: VerifyTokenDTO) -> Optional[Dict[str, Any]]:
        """Decode and validate a JWT, returning the payload or None."""
        try:
            decoded = jwt.decode(dto.token, self.SECRET_KEY, algorithms=[BaseConfig().JWT_ALGORITHM])
            return decoded
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def register_user(self, dto: RegisterUserDTO) -> Dict[str, Any]:
        """Register a new user via client layer."""
        data = {
            "id": dto.id,
            "first_name": dto.first_name,
            "last_name": dto.last_name,
            "email": dto.email,
            "phone_number": dto.phone_number,
            "reputation_score": dto.reputation_score,
        }
        return self.user_client.insert_user(data)

    def create_system_user(self, dto: CreateSystemUserDTO) -> Dict[str, Any]:
        """Create a system user via client layer."""
        data = {
            "system_user_name": dto.system_user_name,
            "password": dto.password,
            "role": dto.role,
        }
        return self.user_client.insert_system_user(dto.user_id, data)

    def is_system_user_exist(self, username: str) -> bool:
        """Check if a system user exists by username."""
        result = self.user_client.get_system_user_by_name(username)
        return result is None
