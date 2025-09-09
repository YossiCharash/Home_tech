from dataclasses import dataclass
from typing import Optional


@dataclass
class LoginRequestDTO:
    username: str
    password: str


@dataclass
class VerifyTokenDTO:
    token: str


@dataclass
class RegisterUserDTO:
    id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    reputation_score: int = 0


@dataclass
class CreateSystemUserDTO:
    user_id: int
    system_user_name: str
    password: str
    role: str
