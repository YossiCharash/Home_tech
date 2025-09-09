from typing import Dict, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from beackend.database.models.users import Users
from beackend.database.models.system_user import SystemUsers


class UserClient:
    def __init__(self, session: Session):
        self.session = session

    def get_password_hash(self, username: str):
        """Retrieve the hashed password for a given username."""
        result = self.session.query(SystemUsers.password_hash).filter(SystemUsers.system_username == username).first()
        return result[0] if result else None

    def insert_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new Users row and return a result dict with status and data/error."""
        user_external_id = data.get("id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        phone_number = data.get("phone_number")
        reputation_score = data.get("reputation_score", 0)

        if not user_external_id or not last_name or not first_name or not email or not phone_number:
            return {"status": 400, "error": "Missing required fields"}

        new_user = Users(
            id=user_external_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            reputation_score=reputation_score
        )

        try:
            self.session.add(new_user)
            self.session.flush()
            user_id = new_user.internal_id
            self.session.commit()
            return {"status": 201, "user_id": user_id}
        except IntegrityError:
            self.session.rollback()
            return {"status": 409, "error": "Username already exists"}
        except Exception as exc:
            self.session.rollback()
            return {"status": 500, "error": f"An error occurred: {str(exc)}"}
        finally:
            self.session.close()

    def insert_system_user(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new SystemUsers row for a given real user id."""
        system_user_name = data.get("system_user_name")
        password = data.get("password")
        role = data.get("role")

        if not system_user_name or not password or not role:
            return {"status": 400, "error": "Missing required fields"}

        hashed_password = generate_password_hash(password)

        system_user = SystemUsers(
            system_username=system_user_name,
            password_hash=hashed_password,
            role=role,
            user_id=user_id
        )

        try:
            self.session.add(system_user)
            self.session.commit()
            return {"status": 201, "system_user_id": system_user.id}
        except IntegrityError as e:
            self.session.rollback()
            return {"status": 409, "error": "System username already exists"}
        except Exception as exc:
            self.session.rollback()
            return {"status": 500, "error": f"An error occurred: {str(exc)}"}
        finally:
            self.session.close()

    def get_system_user_by_name(self, name: str):
        """Retrieve a system user by their username."""
        return self.session.query(SystemUsers).filter(SystemUsers.system_username == name).first()
