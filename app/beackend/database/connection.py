from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.beackend.config import BaseConfig
from app.beackend.database import Base


class Connection:
    _instance = None  # Singleton instance

    def __new__(cls, connection_string: str = BaseConfig().get_connection()):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(connection_string, echo=False)
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            # Create all tables in the database
            Base.metadata.drop_all(cls._instance.engine)
            Base.metadata.create_all(cls._instance.engine)
        return cls._instance

    def get_session(self) -> Session:
        # Create a new session for each call
        return self.Session()